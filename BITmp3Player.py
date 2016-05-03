#!/usr/bin/env python
#Raspberry Pi mp3 player

import os,glob
import RPi.GPIO as GPIO
from time import sleep
import subprocess
print "Running BITmp3Player.py script"
sleep(40)
pausePlyBtn=17
stopBtn=27
nextBtn=19
previousBtn=26
prevInput=0
path= "/mnt/usb/BIT"
run=1#script runs
decider=0#decide which music to run
stop=0
GPIO.setmode(GPIO.BCM)
GPIO.setup(pausePlyBtn,GPIO.IN)#Pause
GPIO.setup(stopBtn,GPIO.IN)#stop
GPIO.setup(nextBtn,GPIO.IN)#next
GPIO.setup(previousBtn,GPIO.IN)#previous

os.chdir(path)#change directory
mp3Files=glob.glob("*.mp3")#finds all mp3 files
listMp3=len(mp3Files)#list
#os.system("tvservice -o")
if (listMp3 <= 0):
    print "Unable to find Mp3 files"
    
while True:
   
    if run==1:
      omx= subprocess.Popen(["omxplayer","-o","local",mp3Files[decider]],stdin=subprocess.PIPE)
      print "songs "+mp3Files[decider]
      proc=omx.poll()
      run=0
      stop=0
      sleep(1)
      
    if(GPIO.input(pausePlyBtn)==True):
      proc=omx.poll()
      if proc !=0:
       omx.stdin.write("p")#pause or play
       print "playing "+mp3Files[decider]
       sleep(1)
          
    if(GPIO.input(stopBtn)==True):
        proc=omx.poll()
        if proc !=0:
            omx.stdin.write("q")#stop
            print "stop playing "+mp3Files[decider]
            os.system("pkill omxplayer")
            stop=1
            sleep(1)
            
            
    if(GPIO.input(nextBtn)== True):
        if stop==0:
          omx.stdin.write("q")
          run=1
          os.system("pkill omxplayer")
          decider=decider+1
        if decider>listMp3 - 1:
              decider=0
              sleep(1)
              
    if (GPIO.input(previousBtn)==True):
         if stop==0:
             omx.stdin.write("q")
             run=1
             os.system("pkill omxplayer")
             decider=decider-1
             if decider<0:
                 decider=0
                 sleep(1)
    else:
        proc =omx.poll()
        if (proc==0 and stop==0):
            run=1
            decider=decider+1
            if decider>listMp3-1:
                decider=0
sleep(1)
