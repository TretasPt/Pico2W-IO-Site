import json
from machine import Pin

class IOInterface:
    def __init__(self,pin:Pin,name:str,pin_id):
        self.__pin_id = pin_id
        self.__pin = pin
        self.__name = name
        
    def __str__(self) -> str:
        return self.__name
    
    def json(self) -> str:
        return "{'error':'IOInterface is not meant to be used directly, use IOInterfaceOUT or IOInterfaceIN instead'}"
    
    def getValue(self) -> int:
        return self.__pin.value()
    
    def runOperation(self,operation:str)  -> tuple[str,str]:
        return "400 Invalid request" , "IOInterface is not meant to be used directly, use IOInterfaceOUT or IOInterfaceIN instead"

    def getId(self) -> str:
        return self.__pin_id

class IOInterfaceOUT(IOInterface):
    def __init__(self, pin_id:int, name, value = False):
        self.__pin_id = pin_id
        pin = Pin(pin_id,Pin.OUT,value=value)
        super().__init__(pin, name,pin_id)

    def json(self) -> str:
        jsonDict = {
            "id":self.__pin_id,
            "io_type":"OUT",
            "name":str(self),
            'value': str(bool(self.getValue())),
        }
        return json.dumps(jsonDict)

    def runOperation(self, operation: str)  -> tuple[str,str]:
        if(operation == "on"):
            self.__pin.on()
        elif(operation == "off"):
            self.__pin.off()
        elif(operation == "toggle"):
            self.__pin.toggle()
        else:
            return "400 Invalid request" , "IOInterfaceOUT has no " + operation + " operation."
        return "200 Success" , self.__name + " set to " + str(bool(self.getValue()))


class IOInterfaceIN(IOInterface):
    def __init__(self, pin_id:int, name, pull = Pin.PULL_DOWN):
        pin = Pin(pin_id,Pin.IN,pull=pull)
        super().__init__(pin, name,pin_id)

    def json(self) -> str:
        jsonDict = {
            "id":self.__pin_id,
            "io_type":"IN",
            "name":str(self),
            'value': str(bool(self.getValue())),
        }
        return json.dumps(jsonDict)

    def runOperation(self,operation:str)  -> tuple[str,str]:
        return "400 Invalid request" , "IOInterfaceIN has no availeable operations."
