import network
import socket
import json
from time import sleep
from machine import Pin
from myconfig import getWifi,getInterfacesJSON,runAction
from utils import bin_blink

#Variables
ssid, password = getWifi()
led_one = Pin(14, Pin.OUT)
led_two = Pin(15, Pin.OUT)

def formatResponse(status,mimeType,body):
    response = b"HTTP/1.0 " + status + "\nContent-type: " + mimeType + "\n\n" + body
    return response

def serveFile(request):
    # print("request: ",request,"\n")
    parts = request.split(" ")

    if parts[0][2:] == "GET":
        if parts[1] == "/":
            f = open("site.html", "r")
            website = f.read()
            return formatResponse("200 OK","text/html",website)
        elif parts[1] == "/favicon.ico":
            f = open("favicon.ico", "rb")
            website = f.read()
            return formatResponse("200 OK","image/x-icon",website)
        elif parts[1] == "/site.css":
            f = open("site.css", "r")
            website = f.read()
            return formatResponse("200 OK","text/css",website)
        elif parts[1] == "/site.js":
            f = open("site.js", "r")
            website = f.read()
            return formatResponse("200 OK","text/js",website)
        elif parts[1] == "/data.json":
            # f = open("site.js", "r")
            # website = f.read()
            # website = '{"data":["todo"]}'
            return formatResponse("200 OK","application/json",getInterfacesJSON())
        else:
            return formatResponse("400 Bad request","text/html","Unknown GET request " + parts[1])
    if(parts[0][2:] == "POST"):

        content = request[request.find("{"):request.find("}")+1].replace("\\r","").replace("\\n","").strip()
        print("content: ",content)
        contentDict = json.loads(content)
        print("contentDict: ",contentDict)
        
        if('target' in contentDict and 'value' in contentDict):
            # if(contentDict['target'] == "led1"):
            #     target = led_one
            # elif(contentDict['target'] == "led2"):            
            #     target = led_two
            # else:
            #     return formatResponse("400 Bad request","text/html","400 - Unknown target " + contentDict.target)
            
            # if(contentDict['value'] == "on"):
            #     target.on()
            # elif(contentDict['value'] == "off"):
            #     target.off()
            # elif(contentDict['value'] == "toggle"):
            #     target.toggle()
            # else:
            #     return formatResponse("400 Bad request","text/html","400 - Unknown value " + contentDict.value)
            
            # return formatResponse("200 OK","text/text","target " + contentDict['target'] + " set to " + str(target.value()))

            resultStatus, resultMessage = runAction(contentDict['target'],contentDict['value'])
            return formatResponse(resultStatus,"text/text",resultMessage)

        else:
            return formatResponse("400 Bad request","text/html", "Wrong format. Expected target and value.")
    
    return formatResponse("500 Internal server error", "text/html","Internal error on function serveFile")

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
            
            cl.send(serveFile(request))
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