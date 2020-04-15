import socket
import sys
import time
import binascii
import threading


class PLCServer:
    def __init__(self, ip, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket successfully created")

        # reserve a port on your computer in our
        # case it is 12345 but it can be anything
        self.port = port
        self.ip = ip

        # Next bind to the port
        # we have not typed any ip in the ip field
        # instead we have inputted an empty string
        # this makes the server listen to requests
        # coming from other computers on the network
        self.s.bind((self.ip, self.port))
        print("socket binded to %s" %(port))

        # put the socket into listening mode
        self.s.listen(1)
        print("socket is listening")
        self.message = "11010110000000001100000000000000"
        self.addr = None
        self.c = None
        self.kill = False

    #hex to binary
    def process_hex(self, message):
        return bin(int(message, 16))[2:].zfill(8)

    #binary to hex
    def process_binary(self, message):
        return hex(int(message, 2))

    #int to binary
    def process_int(self, message):
        return "{0:b}".format(37).zfill(8)

    def receive(self):
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
                #print("BYTE ARRAY:" + message)
                #print("BINARY STRING:" + remainder)

    def scenario_send(self):
        while self.c is None and self.addr is None:
            pass
        conf = hex(int(self.message, 2))
        last = bytearray.fromhex(conf[2:])
        self.c.send(last)
        #print("BYTE ARRAY:" + last)
        #print("BINARY STRING:" + conf)
        start = time.time()
        while time.time() - start < 12:
           begin = time.time()
           while time.time() - begin < 0.44:
               conf = hex(int(self.message, 2))
               last = bytearray.fromhex(conf[2:])
               self.c.send(last)
               #print("BYTE ARRAY:" + last)
               #print("BINARY STRING:" + conf)
               time.sleep(0.05)
           if self.message[0] == "1":
               self.message = "0" + self.message[1:]
           else:
               self.message = "1" + self.message[1:]

        self.message = self.message[0:18] + "1" + self.message[19:]
        while not self.kill:
            begin = time.time()
            while time.time() - begin < 0.44:
               conf = hex(int(self.message, 2))
               last = bytearray.fromhex(conf[2:])
               self.c.send(last)
               #print("BYTE ARRAY:" + last)
               #print("BINARY STRING:" + conf)
               time.sleep(0.05)
            if self.message[0] == "1":
               self.message = "0" + self.message[1:]
            else:
               self.message = "1" + self.message[1:]

    def thread_links(self):
        print("This is a simulation (in messages) of a standard scenario.")
        print("begin by waiting for a plc signal..")
        Thread1 = threading.Thread(target=self.receive, kwargs={})
        Thread2 = threading.Thread(target=self.scenario_send, kwargs={})
        Thread1.start()
        Thread2.start()
        Thread1.join()
        Thread2.join()

if __name__ == "__main__":
    F = PLCServer('127.0.0.1', 12345)
    F.thread_links()
