import json
from machine import Pin

class IOInterface:
    def __init__(self,pin:Pin,name:str):
        self.__pin = pin
        self.__name = name
        
    def __str__(self) -> str:
        return self.__name
    
    def json(self) -> str:
        return ""
    
    def getValue(self) -> int:
        return self.__pin.value()
    
    def runOperation(self,operation:str) -> None:
        pass

class IOInterfaceOUT(IOInterface):
    def __init__(self, pin_id:int, name, value = False):
        self.__pin_id = pin_id
        pin = Pin(pin_id,Pin.OUT,value=value)
        super().__init__(pin, name)

    def json(self) -> str:
        jsonDict = {
            "id":self.__pin_id,
            "io_type":"OUT",
            "name":str(self),
        }
        return json.dumps(jsonDict)

    def runOperation(self, operation: str) -> None:
        if(operation == "on"):
            super().__pin.on()
        elif(operation == "off"):
            super().__pin.off()
        elif(operation == "toggle"):
            super().__pin.toggle()
        # return super().runOperation(operation)
class IOInterfaceIN(IOInterface):
    def __init__(self, pin_id:int, name, pull = Pin.PULL_DOWN):
        self.__pin_id = pin_id
        pin = Pin(pin_id,Pin.IN,pull=pull)
        super().__init__(pin, name)

    def json(self) -> str:
        jsonDict = {
            "id":self.__pin_id,
            "io_type":"IN",
            "name":str(self),
        }
        return json.dumps(jsonDict)
