import network
import socket
import json
from time import sleep
from machine import Pin
from myconfig import getWifi,getInterfacesJSON,runAction
from utils import bin_blink

#Variables
ssid, password = getWifi()
# led_one = Pin(14, Pin.OUT)
# led_two = Pin(15, Pin.OUT)
SSEClients = []

def formatSSE(data:str,tag:str):
    return data.replace("\n","\n" + tag + ": ")

def formatResponse(status,mimeType:str,body:str) -> str:
    response = b"HTTP/1.0 " + status + "\nContent-type: " + mimeType + "\n\n" + body
    return response

def serveFile(request:str) -> tuple [str,bool|None]:
    # print("request: ",request,"\n")
    parts = request.split(" ")

    if parts[0][2:] == "GET":
        if parts[1] == "/":
            f = open("site.html", "r")
            website = f.read()
            return formatResponse("200 OK","text/html",website), None
        elif parts[1] == "/favicon.ico":
            f = open("favicon.ico", "rb")
            website = f.read()
            return formatResponse("200 OK","image/x-icon",website), None
        elif parts[1] == "/site.css":
            f = open("site.css", "r")
            website = f.read()
            return formatResponse("200 OK","text/css",website), None
        elif parts[1] == "/site.js":
            f = open("site.js", "r")
            website = f.read()
            return formatResponse("200 OK","text/js",website), None
        elif parts[1] == "/data.json":
            return formatResponse("200 OK","application/json",getInterfacesJSON()), None
        elif parts[1] == "/dataSSE.json":
            return formatResponse("200 OK","text/event-stream","event: change\ndata:" + formatSSE(getInterfacesJSON(),"data") + "\n\n"), True
        else:
            return formatResponse("400 Bad request","text/html","Unknown GET request " + parts[1]), None
    if(parts[0][2:] == "POST"):

        content = request[request.find("{"):request.find("}")+1].replace("\\r","").replace("\\n","").strip()
        # print("content: ",content)
        contentDict = json.loads(content)
        # print("contentDict: ",contentDict)
        
        if('target' in contentDict and 'value' in contentDict):
            resultStatus, resultMessage = runAction(contentDict['target'],contentDict['value'])
            for con,addr in SSEClients:
                print("updating client ",addr)
                con.send(formatResponse("200 OK","text/event-stream","event: change\ndata:" + formatSSE(getInterfacesJSON(),"data") + "\n\n"))
            return formatResponse(resultStatus,"text/text",resultMessage), None

        else:
            return formatResponse("400 Bad request","text/html", "Wrong format. Expected target and value."), None
    
    return formatResponse("500 Internal server error", "text/html","Internal error on function serveFile"), None

def main():
    # Setup wifi connection
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    max_wait = 30
    print('Waiting for connection')
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        sleep(1)
    status = None
    if wlan.status() != 3:
        raise RuntimeError('Connections failed')
    else:
        status = wlan.ifconfig()
        print('connection to', ssid,'succesfull established!', sep=' ')
        print('IP-adress: ' + status[0])
    ipAddress = status[0]
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    try:
        s = socket.socket()
        s.bind(addr)
        s.listen(1)
    except Exception as error:
        s.close()
        raise RuntimeError('Socket creation failed.')
    
    bin_blink(3,"Starting main loop.")

    while True:
        try:
            cl, addr = s.accept()
            print('Connection from ', addr, "accepted!")
            request = cl.recv(1024)
            request = str(request)
            
            response,stayAlive = serveFile(request)
            if(stayAlive):
                cl.send(response)
                SSEClients.append((cl,addr))
            else:
                cl.send(response)
                cl.close()
                
            
        except OSError as e:
            cl.close()
            print('connection closed')
        except KeyboardInterrupt as e:
            print("Program finished by user.")
            cl.close()
            break

    # s.
    s.close()
    bin_blink(4,"Exiting main loop.")


if __name__ == "__main__":
    main()