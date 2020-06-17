import socket
import sys
import time
import binascii
import threading
from datetime import datetime

class PLCServer:
    """
    Creates a Fake PLC Server the Robot Client can connect to
    """
    def __init__(self, ip, port):
        """
        Creates the socket server for the PLC
        """
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(str(datetime.now()) + " Socket successfully created")

        self.port = port
        self.ip = ip
        self.s.bind((self.ip, self.port))
        print("socket binded to %s" %(port))

        self.s.listen(1)
        print(str(datetime.now()) + " socket is listening")
        self.message = "11010110000000001100000000000000"
        self.addr = None
        self.c = None
        self.kill = False

    def process_hex(self, message):
        """
        Inputs:   String   A hex number as a String
        Outputs:  String   A binary number with 8 bits as a String
        """
        return bin(int(message, 16))[2:].zfill(8)

    def process_binary(self, message):
        """
        Inputs:   String   A binary number as a String
        Outputs:  String   A hex number as a String
        """
        return hex(int(message, 2))

    def process_int(self, message):
        """
        Inputs:   int      An integer
        Outputs:  String   A binary number with 8 bits as a String
        """
        return "{0:b}".format(37).zfill(8)

    def receive(self):
        """
        Waits for a connection then continuously receives 4 bytes at a time
        until the socket disconnects
        """
        while self.addr == None:
           self.c, self.addr = self.s.accept()
        print('Got connection from', self.addr)
        with self.c:
            while not self.kill:
                message = None
                begin = time.time()
                while message is None and time.time() - begin < 1.0:
                    try:
                        message = self.c.recv(4)
                    except socket.error as exc:
                        message = None
                try:
                    remainder = self.process_hex(binascii.hexlify(message)).zfill(32)
                except:
                    remainder = "0" # binascii doesnt react very well if message is empty
                    message = "0"
                    self.kill = True
                #print(str(datetime.now()) + " BYTE ARRAY:" + message)
                #print(str(datetime.now()) + " BINARY STRING:" + remainder)

    def scenario_send(self):
        """
        Waits for a connection
        continuously sends hardcoded messages to the Robot
        """
        while self.c is None and self.addr is None:
            pass
        conf = hex(int(self.message, 2))
        last = bytearray.fromhex(conf[2:])
        try:
            self.c.send(last)
        except:
            self.kill = True
        #print(str(datetime.now()) + " BYTE ARRAY:" + last)
        #print(str(datetime.now()) + " BINARY STRING:" + conf)
        print(str(datetime.now()) + " plc is waiting for a towel")
        start = time.time()
        while time.time() - start < 5 and not self.kill:
           begin = time.time()
           while time.time() - begin < 0.44:
               conf = hex(int(self.message, 2))
               last = bytearray.fromhex(conf[2:])
               try:
                   self.c.send(last)
               except:
                   self.kill = True
               #print(str(datetime.now()) + " BYTE ARRAY:" + last)
               #print(str(datetime.now()) + " BINARY STRING:" + conf)
               time.sleep(0.05)
           if self.message[0] == "1":
               self.message = "0" + self.message[1:]
           else:
               self.message = "1" + self.message[1:]
        print(str(datetime.now()) + " plc is now holding the towel")
        self.message = self.message[0:18] + "1" + self.message[19:]
        start = time.time()
        while time.time() - start < 4 and not self.kill:
            begin = time.time()
            while time.time() - begin < 0.44:
               conf = hex(int(self.message, 2))
               last = bytearray.fromhex(conf[2:])
               try:
                   self.c.send(last)
               except:
                   self.kill = True
               #print(str(datetime.now()) + " BYTE ARRAY:" + last)
               #print(str(datetime.now()) + " BINARY STRING:" + conf)
               time.sleep(0.05)
            if self.message[0] == "1":
               self.message = "0" + self.message[1:]
            else:
               self.message = "1" + self.message[1:]
        print(str(datetime.now()) + " We will simulate the heartbeat not changing now")
        while not self.kill:
            try:
                self.c.send(last)
            except:
                self.kill = True

    def thread_links(self):
        """
        Creates and runs a thread for the methods:
        receive()
        scenario_send()
        """
        print(str(datetime.now()) + " This is a simulation (in messages) of a standard scenario.")
        print(str(datetime.now()) + " begin by waiting for a robot signal..")
        Thread1 = threading.Thread(target=self.receive, kwargs={})
        Thread2 = threading.Thread(target=self.scenario_send, kwargs={})
        Thread1.start()
        Thread2.start()
        Thread1.join()
        Thread2.join()

if __name__ == "__main__":
    F = PLCServer('127.0.0.1', 12345)
    F.thread_links()
