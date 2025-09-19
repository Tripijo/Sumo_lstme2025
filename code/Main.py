from machine import Pin, PWM
import time

led = Pin(25, Pin.OUT)

Rdis = Pin(27, Pin.IN, Pin.PULL_UP) #0 - detected
Ldis = Pin(26, Pin.IN, Pin.PULL_UP)	#0 - detected

Rline = Pin(28, Pin.IN, Pin.PULL_UP) #1 - detected

Rmot1 = PWM(Pin(21, Pin.OUT))
Rmot2 = PWM(Pin(20, Pin.OUT))
Lmot2 = PWM(Pin(19, Pin.OUT))
Lmot1 = PWM(Pin(18, Pin.OUT))

Rmot1.freq(10000)
Rmot2.freq(10000)
Lmot1.freq(10000)
Lmot2.freq(10000)

Speed = 100 #-100 to 100 

lastDisSeen = 1 #-1=left, 1=right

lastDisTime = 0
lastDisSeenSameTime = 0
lastDisSeenBefore = lastDisSeen

def motorR (speed):
    if speed > 0:
        Rmot1.duty_u16(int(speed*65535/100))
        Rmot2.duty_u16(0)
    else:
        Rmot1.duty_u16(0)
        Rmot2.duty_u16(int(-speed/100*65535))
        
def motorL (speed):
    if speed > 0:
        Lmot1.duty_u16(int(speed/100*65535))
        Lmot2.duty_u16(0)
    else:
        Lmot1.duty_u16(0)
        Lmot2.duty_u16(int(-speed/100*65535))
        


while True:
    
    if Rline.value() == 1:
        motorL(-Speed)
        motorR(-Speed)
        time.sleep(0.4)
        motorL(-Speed)
        motorR(Speed)
        time.sleep(0.2)
    
    elif Ldis.value() == 0 and Rdis.value() == 0:  #both detect
        lastDisSeen = 1
        motorL(Speed)
        motorR(Speed)
        lasDisTime = time.ticks_ms()
        
    #if lastDisSeen != lastDisSeenBefore:
     #       lastDisSeenBefore = lastDisSeen
      #      lastDisSeenSameTime = time.ticks_ms()
            
       # if time.ticks_ms() - lastDisSeenSameTime >= 1000:
        #    motorL(0)
         #   motorR(0)
          #  time.sleep(0.1)
           # motorL(Speed)
            #motorR(Speed)
            #time.sleep(0.1)
           
    elif Ldis.value() == 0: #Left detects
        lastDisSeen = -1
        motorL(Speed * 0.8)
        motorR(Speed)
        lastDisTime = time.ticks_ms()
        time.sleep(0.2)
        
    
    elif Rdis.value() == 0: #Right detects
        lastDisSeen = 1
        motorL(Speed)
        motorR(Speed * 0.8)
        lastDisTime = time.ticks_ms()
        time.sleep(0.2)
        
    elif time.ticks_ms() - lastDisTime <= 1000:
        motorL(lastDisSeen * Speed)
        motorR(-lastDisSeen * Speed)
    
    else:
        motorL(Speed*0.6)
        motorR(Speed)
    
    #print(lastDisSeen)
    #time.sleep(0.1)
    

