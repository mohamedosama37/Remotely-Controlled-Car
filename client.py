#!/usr/bin/env python
# Import socket module 
import socket       
import time         
import sys,tty,termios
import threading

class _Getch:
    def __call__(self):
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch  


class _GetchOneChar:
    def __call__(self):
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(2)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch  





# Create a socket object 
s = socket.socket()          
  
# Define the port on which you want to connect 
port = 12128            
  
# connect to the server on local computer 
s.connect(('192.168.43.7', port))

def KeyboardListener():
	try:
		while True:
			    inkey = _Getch()
			    while True:
				
				k=inkey()
				if k!='':
					print k
				break
				
			    if k=='\x1b':
				 inkey= _GetchOneChar()
				 while True:
				   k=inkey()
				   if k!='':
				      print k
				   break
				 if k=='[A':
				   s.send("up")
				 elif k=='[B':
				   s.send("down")
				 elif k=='[C':
				   s.send("right")
				 elif k=='[D':
				   s.send("left")
			    else:
				 if k=="a":
				      s.send("speed up")
				 if k=="z":
				      s.send("slow down")
				 if k=="q":
				      s.send("increase Turn Rate")
				 if k=="w":
				      s.send("decrease Turn Rate")     
				 print "not an arrow key!"+k
	except KeyboardInterrupt:
	    print("Ctl C pressed - ending program")
def ServerListener():
	try:
		while True:
		    recv_data=s.recv(1024)
		    recv_data2=recv_data.rstrip(' ')
		    print 'Recieved this data from the server'+recv_data2.lstrip(' ')+'\r\n'
	except KeyboardInterrupt:
	    print("Ctl C pressed - ending program")

# receive data from the server 
#print s.recv(1024) 
# close the connection 
#s.close()        

if __name__=='__main__':     
      t1= threading.Thread(target =KeyboardListener)
      t2= threading.Thread(target =ServerListener)
      t1.setDaemon(True)
      t2.setDaemon(True)
      t1.start()
      t2.start()
      while True :
          pass



