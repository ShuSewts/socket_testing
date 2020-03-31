
# Import socket module
import socket
import rospy
import threading

class FakeClient:
    def __init__(self, port):
        rospy.init_node("fake_client", anonymous=True)
        # Create a socket object
        self.s = socket.socket()

        # Define the port on which you want to connect
        self.port = port

        # connect to the server on local computer
        self.s.connect(('127.0.0.1', self.port))
        self.buffer = 128
        self.kill = False

        # receive data from the server
        print self.s.recv(2) # this is 2 bytes
        t1 = threading.Thread(target=self.heartbeat, kwargs={})
        #t1.start()

    def send(self, data): #should be if the length of the data is less than or equal to 2 bytes send it
        if len(data) != 2:
            print("make that message 2 bytes and try again")
        else:
            sent = self.s.send(data)
            if sent == 0:
                raise RuntimeError("socket connection broken")
            print("message sent")

    def receive(self):
        message = self.s.recv(2)
        print(message)
        return (len(message) == 2, message)

    def close(self):
        self.s.close()

    def heartbeat(self):
        #self.s.send(b'HI')
        while not self.kill:
            self.s.send("01")
            if not self.receive()[0]:
                self.kill = True
            rospy.sleep(0.5)
            print("made it here")
            self.s.send("00")
            if not self.receive()[0]:
                self.kill = True
            print("and here")
            rospy.sleep(0.5)

if __name__ == "__main__":
    F = FakeClient(12345)
    #F.send("afaf")
    print(F.receive())
    F.heartbeat()
    F.close()
