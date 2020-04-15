import socket
import sys
import time
import binascii


class PLCServer:
    def __init__(self, ip, port):
        s = socket.socket()
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
        s.bind(('', port))
        print("socket binded to %s" %(port))

        # put the socket into listening mode
        s.listen(5)
        print("socket is listening")

        # a forever loop until we interrupt it or
        # an error occurs
        self.message = "11010110000000001100000000000000"


    def sceanrio_send(self):

        addr = None
        while addr == None:
           c, addr = s.accept()
           print('Got connection from', addr)
        conf = hex(int(message, 2))
        last = bytearray.fromhex(conf[2:])
        c.send(last)

        start = time.time()
        while time.time() - start < 12:
           begin = time.time()
           while time.time() - begin < 0.44:
               conf = hex(int(message, 2))
               last = bytearray.fromhex(conf[2:])
               c.send(last)
               print(conf)
               time.sleep(0.05)
           if self.message[0] == "1":
               self.message = "0" + sefl.message[1:]
           else:
               message = "1" + message[1:]

        self.message = self.message[0:18] + "1" + self.message[19:]
        while True:
            begin = time.time()
            while time.time() - begin < 0.44:
               conf = hex(int(message, 2))
               last = bytearray.fromhex(conf[2:])
               c.send(last)
               print(binascii.hexlify(last))
               time.sleep(0.05)
            if message[0] == "1":
               self.message = "0" + self.message[1:]
            else:
               self.message = "1" + self.message[1:]
        #11010110 00000000 11000000 00000000
        # Close the connection with the client
        #c.close()
