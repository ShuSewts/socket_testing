
# Import socket module
import socket
#import rospy
import threading
import time
import binascii

##ways to make this shit faster
##send longer MESSAGES
##decrease the amount of overhead, if possible
class FakeClient:
    def __init__(self, port):
        #rospy.init_node("fake_client", anonymous=True)
        # Create a socket object
        self.s = socket.socket()

        # Define the port on which you want to connect
        self.port = port

        # connect to the server on local computer
        self.s.connect(('127.0.0.1', self.port))
        self.s.setblocking(0)
        self.buffer = 16
        self.kill = False
        self.status = "10100000000000000100000000000000"
        self.last_plc_heartbeat = "11010110000000001100000000000000"
        self.plc_heartbeat_counter = self.last_plc_heartbeat[0] #made 2 as i dont know if theyll be close enough in time
        self.striker = False
        self.ready = False

    #hex to binary
    def process_hex(self, message):
        return bin(int(message, 16))[2:].zfill(8)

    #binary to hex
    def process_binary(self, message):
        return hex(int(message, 2))

    #int to binary
    def process_int(self, message):
        return "{0:b}".format(37).zfill(8)

    #takes a binary message and sends a hex byte array
    def send(self, data): #give a binary message
        data = self.process_binary(data)
        b = bytearray.fromhex(data[2:])
        try:
            self.s.send(b)
        except socket.error as exc:
            pass

    #receives a hex byte array converts to a binary string
    def receive(self):
        message = None
        begin = time.time()
        while message is None and (time.time() - begin < 1.0):
            try:
                message = self.s.recv(4)
            except socket.error as exc:
                message = None
        try:
            remainder = self.process_hex(binascii.hexlify(message)).zfill(32)
        except:
            remainder = "0"
            message = "0"
        #print(remainder)
        self.last_plc_heartbeat = remainder
        return (len(message) == 4, remainder)

    def close(self):
        print("closing connection")
        self.s.close()

    #gets plc status, kills everything if the heartbeat doesnt change
    def get_plc_status(self):
        while not self.kill:
            begin = time.time()
            while time.time() - begin < 0.44:
                temp = self.receive()
            if temp[1][0] == self.plc_heartbeat_counter:
                print("the heartbeat hasnt changed in a half a second")
                self.striker = True
            else:
                self.plc_heartbeat_counter = temp[1][0]
            if self.striker:
                self.kill = True

    #sends status to plc, changes heartbeat of gaming machine every half second
    def send_status(self):
        while not self.kill:
            time1 = time.time()
            while time.time() - time1 < 0.44:
                self.send(self.status) #long binary string
                #print(self.status)
                time.sleep(0.05)
            if self.status[0] == "0":
                self.status = "1" + self.status[1:]
            else:
                self.status = "0" + self.status[1:]

    def scenario(self, message):
        print("Step 1: waiting for run signal from plc..")
        while message is None and self.last_plc_heartbeat[16] != "1" and not self.kill:
            message = self.receive()
        print("Step 2: plc is alive, robot is grabbing the towel. This will take 10 seconds..")
        begin = time.time()
        while(time.time()- begin < 10) and self.last_plc_heartbeat[17] == "1" and not self.kill:
            self.status = self.status[0] + "0100000000000000100000000000000"
        print("Step 3: towel ready for plc")
        self.status = self.status[0] + "0100000000000001000000000000000"
        while self.last_plc_heartbeat[18] != "1" and not self.kill:
            pass
            #print(self.last_plc_heartbeat[18])
        print("Step 4: tcp will now move out of the target position. This will take a second...")
        begin = time.time()
        while time.time() - begin < 1 and not self.kill:
            pass
        self.status = self.status[0] + "0100000000000000000000000000000"
        print("Step 5: axis handles the towel")
        time.sleep(5)
        #begin = time.time()
        #while not self.kill and (time.time() - begin < 10):
        #    pass
        self.kill = True
        self.close()

    def killable_scenarios(self):
        print("we only have the heartbeat right now")

    def thread_links(self):
        time.sleep(1)
        print("This is a simulation (in messages) of a standard scenario.")
        print("begin by waiting for a plc signal..")
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
    F = FakeClient(12345)
    #F.send_status()
    #F.get_plc_status()
    F.thread_links()
    #print(F.receive())
    #print(F.receive())
    #F.close()
