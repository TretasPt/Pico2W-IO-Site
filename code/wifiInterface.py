class wifiInterface:
    def __init__(self,ssid,password)->None:
        self.ssid = ssid
        self.password = password

    def getWifi(self):
        return self.ssid, self.password
