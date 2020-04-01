
# Import socket module
import socket
import rospy
import threading
import time

class FakeClient:
    def __init__(self, port):
        rospy.init_node("fake_client", anonymous=True)
        # Create a socket object
        self.s = socket.socket()

        # Define the port on which you want to connect
        self.port = port

        # connect to the server on local computer
        self.s.connect(('127.0.0.1', self.port))
        self.buffer = 16
        self.kill = False
        self.status = None
        self.last_plc_heartbeat = None
        self.counter = 0
        self.plc_counter = 0 #made 2 as i dont know if theyll be close enough in time
        # receive data from the server
        #print self.s.recv(16) # this is 2 bytes
        t1 = threading.Thread(target=self.heartbeat, kwargs={})
        #t1.start()

    def send(self, data): #data should be a byte array
        b = bytearray()
        b.extend(map(ord, data))
        s.send(b)
        print("should have sent")

    def receive(self):
        message = None
        begin = time.time()
        while message == None and time.time() - begin < 1.0:
            message = self.s.recv(16)
        print(message)
        return (len(message) == 16, message)

    def close(self):
        self.s.close()

    def get_plc_status(self):
        while not self.kill:
            temp = self.receive()
            self.counter2 = self.counter2 +1
            if counter == 20:
                counter = 0
                if temp[1][0] == self.last_plc_heartbeat[0]:
                    print("the heartbeat hasnt changed in a second")
                    self.kill = True
            self.last_plc_heartbeat = temp[1]
            rospy.sleep(0.05)
            if not temp[0]:
                print("we waited a whole second for a message")
                self.kill

    def send_status(self):
        while not self.kill:
            self.send(self.status)
            #something to set the status
            rospy.sleep(0.05)
            self.counter = self.counter +1

if __name__ == "__main__":
    F = FakeClient(12345)
    #F.send("afaf")
    print(F.receive())
    F.heartbeat()
    F.close()
