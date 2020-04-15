
# first of all import the socket library
import socket#
import sys
#sys.path.append('/opt/ros/kinetic/lib/python2.7/dist-packages')
#import rospy
import time
import binascii
#sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')

#rospy.init_node("fake_plc", anonymous=True)

# next create a socket object
s = socket.socket()
print("Socket successfully created")

# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12345

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

   # Establish connection with client.
counter = 0
message = "11010110000000001100000000000000"
addr = None
while addr == None:
   c, addr = s.accept()
   print('Got connection from', addr)
conf = hex(int(message, 2))
last = bytearray.fromhex(conf[2:])
c.send(last)

#FOR NO MESSAGES AFTER A WHILE
#c.send('sphynxofblackquasphynxofblackquasphynxofblackquasphynxofblackquasphynxofblackquasphynxofblackquasphynxofblackquasphynxofblackqua')
#FOR UNCHANGING HEARTBEATS
#c.send('sphynxofblackquasphynxofblackquasphynxofblackquasphynxofblackquasphynxofblackquasphynxofblackquasphynxofblackquasphynxofblackquasphynxofblackquasphynxofblackquasphynxofblackquasphynxofblackqua')
#c.send('sphynxofblackquasphynxofblackquasphynxofblackquasphynxofblackquasphynxofbla ckquasphynxofblackquasphynxofblackquasphynxofblackquasphynxofblackquasphynxofblackquasphynxofblackquasphynxofblackqua')
#while True:
   #message = message[0] + "1010110000000001100000000000000"
start = time.time()
while time.time() - start < 12:
   begin = time.time()
   while time.time() - begin < 0.44:
       conf = hex(int(message, 2))
       last = bytearray.fromhex(conf[2:])
       c.send(last)
       print(binascii.hexlify(last))
       time.sleep(0.05)
   if message[0] == "1":
       message = "0" + message[1:]
   else:
       message = "1" + message[1:]

message = message[0:18] + "1" +message[19:]
print(message[18])
while True:
    begin = time.time()
    while time.time() - begin < 0.44:
       conf = hex(int(message, 2))
       last = bytearray.fromhex(conf[2:])
       c.send(last)
       print(binascii.hexlify(last))
       time.sleep(0.05)
    if message[0] == "1":
       message = "0" + message[1:]
    else:
       message = "1" + message[1:]
#11010110 00000000 11000000 00000000
# Close the connection with the client
#c.close()
