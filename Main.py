import threading
import serial
import datetime
from time import sleep
from queue import Queue

commands = Queue()
finish = Queue()
turns = Queue()

VALID_INSTRUC = ("start", "stop", "setTime", "getTime",
                "setMode", "getMode", "exit", "help" )                

VALID_MODES = ("readAll", "onlyTemp", "onlyHum")

DESC_INSTRUC = { "start": "Begins the capture of data sent by the Arduino.", 
                "stop": "Stop the capture of data from Arduino.", 
                "setTime": "Modify the Delay between one capture an the next one.", 
                "getTime": "Show the Delay time.",
                "setMode": "Modify the capture mode, between: readAll, onlyTemp and onlyHum.", 
                "getMode": "Por implementar...",
                "exit": "Por implementar...", 
                "help": "Por implementar..."  }

arduino = None
try:
    arduino = serial.Serial("COM4", 9600)
    sleep(2)
except:
    print("No se detecto el dispositivo")

def write_command():
    while True:
        if turns.empty():         
            instruc = input(">")
            if instruc in VALID_INSTRUC:
                if instruc == "help":
                    show_help()
                else:
                    commands.put(instruc)
                    turns.put("tr")
            else:
                print("El comando \"{}\" no es valido.".format(instruc))        
            if instruc == "exit":
                break

def show_help(instr=""):
    for i in DESC_INSTRUC.keys():
        print("{}: {}".format(i, DESC_INSTRUC[i]))

def run_driver():
    """ This function implement the operation of the driver """
    while True:
        instruc = ""
        if not commands.empty():
            instruc = commands.get()
        if instruc == "start":
            star()
        if instruc == "stop":
            stop()
        if instruc == "setTime":
            set_time()
        if instruc == "getTime":
            get_time()
        if instruc == "setMode":
            set_mode()
        if instruc == "getMode":
            get_mode()
        if instruc == "exit":
            break

def star():
    arduino.write(b'start')
    finish.put("read")
    rs = threading.Thread(target=read_serial)
    rs.start()
    turns.get()

def stop():
    arduino.write(b'stop')
    finish.get()
    turns.get()

def set_time():
    arduino.write(b'setTime')
    n_time = input("\tNew delay(ms): ")
    arduino.write(n_time.encode())
    turns.get()

def get_time():
    arduino.write(b'getTime')
    r_ardu = arduino.readline()
    print(r_ardu.decode())
    turns.get()

def set_mode():
    arduino.write(b'setMode')
    while True:
        n_mode = input("Write the new mode: ")
        if  n_mode in VALID_MODES:
            break
        else:
            print("The mode \"{}\" is not a valid mode".format(n_mode))
    arduino.write(n_mode.encode())
    turns.get()

def get_mode():
    arduino.write(b'getMode')
    r_ardu = arduino.readline()
    print(r_ardu.decode())
    turns.get()

def write_file(info=""):    
    now = datetime.datetime.now()
    name = "{}-{}-{}.txt".format(now.year, now.month, now.day)
    f = open(name, 'a')
    if info != "":
        f.write(info)
        f.write('\n')
    f.close()

def read_serial():
    while not finish.empty():
        r_ardu = arduino.readline()
        write_file(r_ardu.decode())


if __name__ == '__main__':    
    w = threading.Thread(target=write_command)
    r = threading.Thread(target=run_driver)

    r.start()
    w.start()    