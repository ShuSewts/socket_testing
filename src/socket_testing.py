import socket
import sys
import time
import binascii
import threading


class PLCServer:
    def __init__(self, ip, port):
        self.s = socket.socket()
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
        self.s.listen(5)
        print("socket is listening")

        # a forever loop until we interrupt it or
        # an error occurs
        self.message = "11010110000000001100000000000000"
        self.addr = None
        self.c = None


    def scenario_send(self):
        while self.addr == None:
           self.c, self.addr = self.s.accept()
           print('Got connection from', self.addr)
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
        while True:
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

    def receive(self):
        while self.c is None and self.addr is None:
            pass
        while True:
            message = None
            begin = time.time()
            #max time we wait for a message is 1 second
            while message is None and (time.time() - begin < 1.0):
                try:
                    message = self.s.recv(4)
                except socket.error as exc:
                    message = None #force s.recv() if we get a socket error
            try:
                remainder = self.process_hex(binascii.hexlify(message)).zfill(32)
            except:
                remainder = "0" # binascii doesnt react very well if message is empty
                message = "0"
            #print("BYTE ARRAY:" + message)
            #print("BINARY STRING:" + remainder)
            self.last_plc_heartbeat = remainder
            return (len(message) == 4, remainder)

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
    F = PLCServer('', 12345)
    F.thread_links()
