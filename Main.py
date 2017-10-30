import threading
import serial
from time import sleep
from queue import Queue

commands = Queue()

VALID_INSTRUC = ("start", "stop", "setTime", "getTime",
                "setMode", "getMode", "exit", "help"
                )                

VALID_MODES = ("readAll", "onlyTemp", "onlyHum")

instruc_descrip = { "start": "Por implementar...", 
                    "stop": "Por implementar...", 
                    "setTime": "Por implementar...", 
                    "getTime": "Por implementar...",
                    "setMode": "Por implementar...", 
                    "getMode": "Por implementar...",
                    "exit": "Por implementar...", 
                    "help": "Por implementar..."
                }

def write_command():
    while True:        
        instruc = input(">")
        if instruc in VALID_INSTRUC:
            if instruc == "help":
                show_help()
            else:
                commands.put(instruc)        
        else:
            print("El comando \"{}\" no es valido.".format(instruc))        
        if instruc == "exit":
            break

def show_help(instr=""):
    for i in instruc_descrip.keys():
        print("{}: {}".format(i, instruc_descrip[i]))

def run_driver():
    try:
        instruc = "stop"    
        arduino = serial.Serial("COM4", 9600)
        while True:        
            if not commands.empty():                        
                instruc = commands.get()
            if instruc == "exit":                        
                break    
    except:
        print("No se detecto el dispositivo")

if __name__ == '__main__':    
    w = threading.Thread(target=write_command)
    r = threading.Thread(target=run_driver)
    
    r.start()
    w.start()    