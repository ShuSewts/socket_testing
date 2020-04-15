import socket
import threading
import time
import binascii
from datetime import datetime

class RobotClient:
    """
    Creates a Fake Robot Client for connecting to the PLC Socket
    """
    def __init__(self, ip, port):
        """
        Creates the socket object for the Robot
        """
        # Create a socket object
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Define the port on which you want to connect
        self.port = port
        self.ip = ip

        self.s.connect((self.ip, self.port))
        print("socket connected to %s" %(port))
        self.s.setblocking(0)
        self.kill = False
        self.status = "10100000000000000100000000000000"
        self.last_plc_heartbeat = "11010110000000001100000000000000"
        self.plc_heartbeat_counter = self.last_plc_heartbeat[0]
        self.striker = False
        self.ready = False

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

    def send(self, data):
        """
        Inputs:   String   A binary number with 8 bits as a String
        Turns a binary number into a byte array and sends the byte array through the socket connection
        """
        data = self.process_binary(data) #bin to hex
        b = bytearray.fromhex(data[2:]) #hex to hex byte array
        try:
            self.s.send(b)
        except socket.error as exc:
            pass

    def receive(self):
        """
        Receives a byte array via the socket connection and converts to binary string
        """
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
        #print(str(datetime.now()) + " BYTE ARRAY:" + message)
        #print(str(datetime.now()) + " BINARY STRING:" + remainder)
        self.last_plc_heartbeat = remainder
        return (len(message) == 4, remainder)

    def close(self):
        """
        Closes socket connection
        """
        print(str(datetime.now()) + " closing connection")
        self.s.close()

    def get_plc_status(self):
        """
        Requests the status of the PLC every 50ms
        Checks if the heartbeat of the PLC is changing
        If the heartbeat does not change for one second, this method is killed
        """
        while not self.kill:
            begin = time.time()
            while time.time() - begin < 0.44:
                temp = self.receive()
            if temp[1][0] == self.plc_heartbeat_counter:
                print(str(datetime.now()) + " the heartbeat hasnt changed in a half a second")
                self.striker = True
            else:
                self.plc_heartbeat_counter = temp[1][0]
            if self.striker:
                print(str(datetime.now()) + " the heartbeat hasnt changed fora whole second")
                self.kill = True

    def send_status(self):
        """
        Sends status of Robot every 50 ms
        Changes the heartbeat every 500ms
        If the heartbeat of the PLC does not change, this method is killed
        """
        while not self.kill:
            time1 = time.time()
            while time.time() - time1 < 0.44:
                self.send(self.status)
                #print(str(datetime.now()) + self.status)
                time.sleep(0.05)
            if self.status[0] == "0":
                self.status = "1" + self.status[1:]
            else:
                self.status = "0" + self.status[1:]

    def scenario(self, message):
        """
        Creates a Scenario in Simulation
        """
        print(str(datetime.now()) + " Step 1: waiting for run signal from plc..")
        while message is None and self.last_plc_heartbeat[16] != "1" and not self.kill:
            message = self.receive()
        print(str(datetime.now()) + " Step 2: plc is alive, robot is grabbing the towel. This will take 10 seconds..")
        begin = time.time()
        while(time.time()- begin < 10) and self.last_plc_heartbeat[17] == "1" and not self.kill:
            self.status = self.status[0] + "0100000000000000100000000000000"
        print(str(datetime.now()) + " Step 3: towel ready for plc")
        self.status = self.status[0] + "0100000000000001000000000000000"
        while self.last_plc_heartbeat[18] != "1" and not self.kill:
            pass
        print(str(datetime.now()) + " Step 4: tcp will now move out of the target position. This will take a second...")
        begin = time.time()
        while time.time() - begin < 1 and not self.kill:
            pass
        self.status = self.status[0] + "0100000000000000000000000000000"
        print(str(datetime.now()) + " Step 5: axis handles the towel")
        time.sleep(5)
        self.kill = True
        self.close()

    def killable_scenarios(self):
        """
        Placeholder method
        """
        print(str(datetime.now()) + " we only have the heartbeat right now")

    def thread_links(self):
        """
        Creates and runs a thread for the methods:
        send_status()
        get_plc_status()
        scenario()
        """
        time.sleep(1)
        print(str(datetime.now()) + " This is a simulation (in messages) of a standard scenario.")
        print(str(datetime.now()) + " begin by waiting for a plc signal..")
        Thread1 = threading.Thread(target=self.send_status, kwargs={})
        Thread2 = threading.Thread(target=self.get_plc_status, kwargs={})
        Thread3 = threading.Thread(target=self.scenario, kwargs={'message': None})
        Thread1.start()
        Thread2.start()
        Thread3.start()
        Thread1.join()
        Thread2.join()
        Thread3.join()

if __name__ == "__main__":
    F = RobotClient('127.0.0.1', 12345)
    F.thread_links()
