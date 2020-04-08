
# Import socket module
import socket
import rospy
import threading
import time

##ways to make this shit faster
##send longer MESSAGES
##decrease the amount of overhead, if possible
class FakeClient:
    def __init__(self, port):
        rospy.init_node("fake_client", anonymous=True)
        # Create a socket object
        self.s = socket.socket()

        # Define the port on which you want to connect
        self.port = port

        # connect to the server on local computer
        self.s.connect(('127.0.0.1', self.port))
        self.s.setblocking(0)
        self.buffer = 16
        self.kill = False
        self.status = "0000000000000000000000000000000"
        self.last_plc_heartbeat = "0000000000000000000000000000000"
        self.counter = 0
        self.plc_counter = 0 #made 2 as i dont know if theyll be close enough in time

    def send(self, data): #give a binary message
        data = self.process_binary(data)
        b = bytearray.fromhex(data[2:])
        self.s.send(b)
        #print("should have sent")

    def receive(self):
        message = None
        begin = time.time()
        while message == None and (time.time() - begin < 1.0):
            try:
                message = self.s.recv(4)
            except socket.error as exc:
                return (False, "gone")

        remainder = ''
        for thing in message:
            remainder = bin(thing)[2:].zfill(8)

        self.last_plc_heartbeat = remainder
        return (len(message) == 4, remainder)

    def close(self):
        self.s.close()

    def process_hex(self, message):
        return bin(int(message, 16))[2:].zfill(8)

    def process_binary(self, message):
        return hex(int(message, 2))

    def get_plc_status(self):
        while not self.kill:
            temp = self.receive()
            print(temp)
            self.plc_counter = self.plc_counter +1
            if self.plc_counter == 20:
                self.plc_counter = 0
                if temp[1][0] == self.last_plc_heartbeat[0]:
                    print("the heartbeat hasnt changed in a second")
                    self.kill = True
            self.last_plc_heartbeat = temp[1]
            rospy.sleep(0.05)
            if not temp[0]:
                print("we waited a whole second for a message")
                self.kill = True

    def send_status(self):
        while not self.kill:
            self.send(self.status) #long binary string
            rospy.sleep(0.05)
            self.counter = self.counter +1
            if self.counter == 10:
                if self.status[0] == "0":
                    self.status[0] = "1"
                else:
                    self.status[0] = "0"

    def scenario(self):
        while message == None and self.last_plc_heartbeat[16] != "1":
            message = self.receive()
        print("plc is alive, grabbing towel. This will take 10 seconds..")
        begin = time.time()
        while(time.time()- begin < 10) and self.last_plc_heartbeat[17] == "1":
            self.status = self.status[0] + "0100000000000000100000000000000"
        print("towel ready for plc")
        self.status = self.status[0] + "0100000000000001000000000000000"
        while self.last_plc_heartbeat[18] != 1:
            pass
        print("tcp will now move out of the target position. This will take a second...")
        begin = time.time()
        while(time.time()- begin < 1):
            pass
        self.status = self.status[0] + "0100000000000000000000000000000"
        print("axis do your thing")
        begin = time.time()
        while not self.kill and (time.time() - begin < 10):
            pass
        self.kill = True

    def killable_scenarios(self):
        print("we only have the heartbeat right now")

    def thread_links(self):
        print("This is a simulation (in messages) of a standard scenario.")
        print("begin by waiting for a plc signal..")
        message = None
        Thread1 = threading.Thread(target=self.send_status, kwargs={})
        Thread2 = threading.Thread(target=self.get_plc_status, kwargs={})
        Thread3 = threading.Thread(target=self.scenario, kwargs = {})
        Thread1.start()
        Thread2.start()
        Thread1.join()
        Thread2.join()

if __name__ == "__main__":
    F = FakeClient(12345)
    #F.send_status()
    #F.get_plc_status()
    F.thread_links()
    #print(F.receive())
    #print(F.receive())
    F.close()
