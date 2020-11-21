#!/usr/bin/env python
# first of all import the socket library 
import socket 
import time
#import RPi.GPIO as GPIO

# Declare the GPIO settings
#GPIO.setmode(GPIO.BOARD)


# set up GPIO pins
#GPIO.setup(7, GPIO.OUT) # Connected to BIN1
#GPIO.setup(11, GPIO.OUT) # Connected to AIN2
#GPIO.setup(12, GPIO.OUT) # Connected to AIN1
#GPIO.setup(13, GPIO.OUT) # Connected to BIN2  


#pwm = GPIO.PWM(12, 100) 
#pwm1 = GPIO.PWM(13, 100) 
 
# next create a socket object 
s = socket.socket()          
print "Socket successfully created"
  
# reserve a port on your computer in our 
# case it is 12345 but it can be anything 
port = 12128             
  
# Next bind to the port 
# we have not typed any ip in the ip field 
# instead we have inputted an empty string 
# this makes the server listen to requests  
# coming from other computers on the network 
s.bind(('', port))         
print "socket binded to %s" %(port) 
  
# put the socket into listening mode 
s.listen(5)      
print "socket is listening"            
  
# a forever loop until we interrupt it or  
# an error occurs 
while True: 
  
# Establish connection with client. 

   c, addr = s.accept()
   # try:
   while True:
     recv_data=c.recv(1024)
     print 'Recieved this data from the client'+recv_data
      dc = 50
      pwm.ChangeDutyCycle(dc)
      pwm1.ChangeDutyCycle(dc)				# Initialize PWM on pwmPin 100Hz frequency
      pwm.start(dc)                                    # Start PWM with 50% duty cycle
      pwm1.start(dc)                                   # Start PWM with 50% duty cycle

     if recv_data == "up": 
         GPIO.output(11,GPIO.HIGH)
         GPIO.output(12,GPIO.LOW)
         GPIO.output(7,GPIO.HIGH)
         GPIO.output(13,GPIO.LOW)
     elif recv_data == "down":
         GPIO.output(12,GPIO.HIGH)
         GPIO.output(11,GPIO.LOW)
         GPIO.output(13,GPIO.HIGH)
         GPIO.output(7,GPIO.LOW)
     elif recv_data == "right":
         GPIO.output(12,GPIO.HIGH)
         GPIO.output(11,GPIO.LOW)
         GPIO.output(13,GPIO.LOW)
         GPIO.output(7,GPIO.LOW)
     else :
         GPIO.output(12,GPIO.LOW)
         GPIO.output(11,GPIO.LOW)
         GPIO.output(7,GPIO.HIGH)
         GPIO.output(13,GPIO.LOW)
   except KeyboardInterrupt:
  	print("Ctl C pressed - ending program")
   pwm.stop() 
   pwm1.stop()     
   print 'Got connection from', addr 
  
   # send a thank you message to the client.  
   c.send('Thank you for connecting') 
#ultrasonic
   PIN_TRIGGER = 1
   PIN_ECHO = 2

   GPIO.setup(PIN_TRIGGER, GPIO.OUT)
   GPIO.setup(PIN_ECHO, GPIO.IN)

   GPIO.output(PIN_TRIGGER, GPIO.LOW)

   print "Waiting for sensor to settle"

   time.sleep(2)

   print "Calculating distance"

   GPIO.output(PIN_TRIGGER, GPIO.HIGH)

   time.sleep(0.00001)

   GPIO.output(PIN_TRIGGER, GPIO.LOW)

   while GPIO.input(PIN_ECHO)==0:
         pulse_start_time = time.time()
   while GPIO.input(PIN_ECHO)==1:
         pulse_end_time = time.time()

      pulse_duration = pulse_end_time - pulse_start_time
      distance = round(pulse_duration * 17150, 2)
      print "Distance:",distance,"cm"
      c.send("Distance:",distance,"cm") 
      Close the connection with the client 
   c.close() 

