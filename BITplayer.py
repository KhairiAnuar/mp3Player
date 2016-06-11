#!/usr/bin/env python
#Raspberry Pi mp3 player

import os,glob,random
import RPi.GPIO as GPIO
from time import sleep
import subprocess
import eyed3
import Adafruit_CharLCD as LCD
print "Running BITplayer.py script"
sleep(10)

#Raspberry Pi pin configuration:
lcd_rs=18 
lcd_en=23
lcd_d4 =12
lcd_d5 =16
lcd_d6 =20
lcd_d7 =21
pausePlyBtn=4
stopBtn=17
nextBtn=22
previousBtn=27 
volUpBtn=5
volDwnBtn=6
shuffleBtn=13
path= "/media/pi/B228858B28854EF3/BIT"
run=1#script runs
index=0#index music to play
stop=0
shuffle=0
status=1#1 play 0 pause
checkBtn=1


#column and row size for 16x2 LCD.
lcd_width = 16
lcd_height = 2

#Initialize the LCD using pins above
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_width, lcd_height)

#Setup GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(pausePlyBtn,GPIO.IN)#Pause
GPIO.setup(stopBtn,GPIO.IN)#stop
GPIO.setup(nextBtn,GPIO.IN)#next
GPIO.setup(previousBtn,GPIO.IN)#previous
GPIO.setup(volUpBtn,GPIO.IN)#Volume up
GPIO.setup(volDwnBtn,GPIO.IN)#volume down
GPIO.setup(shuffleBtn,GPIO.IN)#shuffle
GPIO.setup(lcd_rs,GPIO.OUT)#registerSelect
GPIO.setup(lcd_en,GPIO.OUT)#enable
GPIO.setup(lcd_d4,GPIO.OUT)#data 4
GPIO.setup(lcd_d5,GPIO.OUT)#data 5
GPIO.setup(lcd_d6,GPIO.OUT)#data 6
GPIO.setup(lcd_d7,GPIO.OUT)#data 7

os.chdir(path)#change directory
mp3Files=glob.glob("*.mp3")#finds all mp3 files
listMp3=len(mp3Files)#list
shuffleList=random.choice(os.listdir("/media/pi/B228858B28854EF3/BIT"))
#shuffleFile=random.shuffle(mp3Files)
#shuffleFile=filter(lambda f: f.endswith(".mp3"),shuffleList)
#os.system("tvservice -o")

lcd.message("Music Player \nby StrawberryPi")  
sleep(1.5)
lcd.clear()#clear LCD
if (listMp3 <= 0):
    print "Unable to find Mp3 files"
  
############################    
#     Start the music      #
############################
while True:
    #play music in alphabetic order
    if run==1 and shuffle ==0:
      lcd.clear()
      omx= subprocess.Popen(["omxplayer","-o","local",mp3Files[index]],stdin=subprocess.PIPE)
      lcd.message("Playing")
      sleep(1)
      lcd.clear()
      songPlaying=eyed3.load(mp3Files[index])#load eyed3
      lcd.message(songPlaying.tag.title+"\n"+ songPlaying.tag.artist)#get metadata from song
      status=1
      run=0
      stop=0
      sleep(1)
      
      #play shuffled music
    if run==0 and shuffle==1:
       lcd.clear()
       random.shuffle(mp3Files)#to shuffle the list of mp3
       omx= subprocess.Popen(["omxplayer","-o","local",mp3Files[index]],stdin=subprocess.PIPE) 
       songPlaying=eyed3.load(mp3Files[index])
       lcd.message("Playing")
       sleep(1)
       lcd.clear()
       lcd.message(songPlaying.tag.title+"\n"+ songPlaying.tag.artist)
       status=1
       stop=0
       shuffle=0
       sleep(1)
       
    #when play or pause is pressed
    if(GPIO.input(pausePlyBtn)==True):
      lcd.clear()
      checkBtn+=1
      proc=omx.poll()
      if proc !=0:
         omx.stdin.write("p")#pause or play
      if checkBtn%2==0: #checks if it is in pause state or play state
           lcd.clear()
           lcd.message("Paused")
           status=0
           sleep(1)
      else:
          lcd.clear()
          lcd.message("Playing")
          sleep(1)
          lcd.clear()
          songPlaying=eyed3.load(mp3Files[index])
          lcd.message(songPlaying.tag.title+"\n"+songPlaying.tag.artist)
          status=1      
          sleep(1) 
      
    #when stop button is pressed
    if(GPIO.input(stopBtn)==True):
        proc=omx.poll()
        if proc !=0:
            lcd.clear()
            omx.stdin.write("q")#stop
            print "stop playing "+mp3Files[index]
            lcd.message("Stopped")
            os.system("pkill omxplayer")
            stop=1
            sleep(2)
            lcd.clear()
            lcd.message("Goodbye!")
            sleep(2)
            lcd.clear()
            #GPIO.cleanup()
      
      #when next button is pressed    
    if(GPIO.input(nextBtn)== True):
        if stop==0:
          lcd.clear()
          omx.stdin.write("q")
          run=1
          os.system("pkill omxplayer")
          index=index+1
          lcd.message("Playing")
          lcd.clear()
          songPlaying=eyed3.load(mp3Files[index])
          lcd.message(songPlaying.tag.title+"\n"+songPlaying.tag.artist) 
       # if len(songPlaying.tag.title)>lcd_width:
       #   for i in range(lcd_width-len(songPlaying.tag.title)):
       #        sleep(0.5)
       #        lcd.move_left()            
        if index>listMp3 - 1:
              index=0
              sleep(1)
              
    #when previous button is pressed plays previous song           
    if (GPIO.input(previousBtn)==True):
         if stop==0:
             omx.stdin.write("q")
             run=1
             os.system("pkill omxplayer")#terminate omxplayer(because multiple omxplayer running) 
             index=index-1
             lcd.message("Playing")
             sleep(1)
             lcd.clear()
             songPlaying=eyed3.load(mp3Files[index])# get song details
             lcd.message(songPlaying.tag.title+"\n"+songPlaying.tag.artist)#display song details on lcd 
         if index<0:
                 index=0
                 sleep(1)
                 
    #Volume up button press
    if (GPIO.input(volUpBtn)==True):
         if stop==0:    
            omx.stdin.write("+")
            sleep(1)
    #Volume down button press        
    if (GPIO.input(volDwnBtn)==True):
         if stop==0:    
            omx.stdin.write("-")
            sleep(1)
            
    #Shuffle button pressed         
    if(GPIO.input(shuffleBtn)==True):
        proc=omx.poll() 
        if stop==0 and proc!=0:
            os.system("pkill omxplayer")
            run=0
            shuffle=1
            sleep(1)
       
    else: #if finished playing go back to beginning song
        proc =omx.poll()
        if (proc==0 and stop==0):
            run=1
            index=index+1
            if index>listMp3-1:
                index=0
sleep(1)
