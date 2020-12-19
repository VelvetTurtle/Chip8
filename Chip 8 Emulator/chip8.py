# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 20:10:56 2020

@author: Beth Fox
The CPU for my Chip 8 emulator. 
"""

#IMPORTS
import pygame, time
import main
from pygame import key
from random import randint
pygame.init()
class Chip8(object):
    #declare fontset as class variable
   fontset = [0xF0, 0x90, 0x90, 0x90, 0xF0, 
	  	0x20, 0x60, 0x20, 0x20, 0x70, 
	  	0xF0, 0x10, 0xF0, 0x80, 0xF0, 
		0xF0, 0x10, 0xF0, 0x10, 0xF0, 
	 	0x90, 0x90, 0xF0, 0x10, 0x10, 
		0xF0, 0x80, 0xF0, 0x10, 0xF0, 
	    0xF0, 0x80, 0xF0, 0x90, 0xF0, 
	    0xF0, 0x10, 0x20, 0x40, 0x40, 
	    0xF0, 0x90, 0xF0, 0x90, 0xF0, 
		0xF0, 0x90, 0xF0, 0x10, 0xF0, 
		0xF0, 0x90, 0xF0, 0x90, 0x90, 
		0xE0, 0x90, 0xE0, 0x90, 0xE0, 
	 	0xF0, 0x80, 0x80, 0x80, 0xF0, 
	    0xE0, 0x90, 0x90, 0x90, 0xE0, 
	    0xF0, 0x80, 0xF0, 0x80, 0xF0, 
	 	0xF0, 0x80, 0xF0, 0x80, 0x80]
   
   def __init__(self):
        self.pc = 0x200  #Program counter, it starts at 0x200 this is the point in memory where most programs of chip8 begin
        self.opcode = 0  #reset current opcode
        self.stack =[0]*16   #empty stack, the stack is used to store return adresses when subroutines are called
        self.idx = 0       #reset index register
        self.sp = 0      #pointer for stack
        self.v = [0]*16 # stores the 16 8 bit registers
        self.memory = [0]*4069 #empty array to represent memory it has 4069 bits to represent 4kb
        self.keys = [0]*16  #empty array that represents the keys
        self.delay_timer = 0 #reset delay timer, is used to time events in the game
        self.sound_timer = 0 #reset sound timer is used for sound effects. When its value is nonzero make a bleep sound
        self.gfx = [0]*64*32 #represents all the pixels on the screen
        self.load_fonts()
        self.draw_flag = True
        self.t_last = time.time()
   #Load the fontset into memory        
   def load_fonts(self):
        for i in range(0,80,1):
            self.memory[i] = self.fontset[i]            
   
   #takes rom filename and takes the binary data from file and stores it
   #into memory starting at 0x200
   def load_rom(self, file_name):
       addr = 0x200
       with open(file_name, 'rb') as file:
           line = file.read()
           for i in range(len(line)):
               self.memory[addr + i] = line[i]
   
   def update_timers(self):
       if(self.delay_timer > 0):
           self.delay_timer = self.delay_timer -1
       if(self.sound_timer > 0):
           self.sound_timer = self.sound_timer - 1  
   def emulate_cycle(self, scr):
       #fetch opcode this works by pulling the first byte of the opcode moving it to the left
       #one byte and then adding the next byte to the end of it
       self.opcode = self.memory[self.pc] << 8 | self.memory[self.pc + 1]
       x = (self.opcode & 0x0F00) >> 8
       kk = self.opcode & 0x00FF
       y = (self.opcode & 0x00F0) >> 4
       for i in self.v:
          print(hex(i))
       print("opcode: ",hex(self.opcode))
       print("pc:", hex(self.pc))
       print("x:", x)
       print("y:", y)
       #Long if else structure that executes a command based on the opcode
       
       #If opcode starts with 0x0
       if(self.opcode & 0xF000 == 0x0000):
           #Op code: 0x00E0 clears the screen
           if(self.opcode == 0x00E0):
               for i in range(len(self.gfx)):
                   self.gfx[i] = 0
               self.draw_flag=True    
           #OPcode: 0x00EE  
           elif(self.opcode == 0x00EE):
               self.sp -= 1
               self.pc = self.stack[self.sp]
           
        #Op code: 1NNN sets program counter to the NNN
       elif(self.opcode & 0xF000 == 0x1000):
           self.pc = self.opcode & 0x0FFF
           self.pc = self.pc -2
        #Op code: 2NNN increments stack pointer puts current pc on top of stack and calls subroutine at nnn
       elif(self.opcode & 0xF000 == 0x2000):
           self.stack[self.sp] = self.pc
           self.sp +=1
           self.pc = self.opcode & 0x0FFF
           self.pc -=2
        #Op code: 3xkk Skips instruction if Vx == kk by incrementing program counter by 2   
       elif(self.opcode & 0xF000 == 0x3000):
           
           if(self.v[x] == kk):
               self.pc +=2
       
        #Op code:4xkk Skips instruction if Vx != kk by incrementing program counter by 2
       elif(self.opcode & 0xF000 == 0x4000):
           if(self.v[x] != kk):
               self.pc +=2
       #Op code:5xy0 skips next instruction if Vx = Vy by incrementing program counter by 2        
       elif(self.opcode & 0xF000 == 0x5000):
           if(self.v[x] == self.v[y]):
               self.pc += 2
       #Op code: 6xkk places the value of kk into register Vx
       elif(self.opcode & 0xF000 == 0x6000):
           self.v[x]= kk
    
       #Op code: 7xkk adds value of kk to the value of Vx and stores that value into Vx
       elif(self.opcode & 0xF000 == 0x7000):
           self.v[x] = kk + self.v[x]
           self.v[x] %= 256
       #If opcode starts with 0x8
       elif(self.opcode & 0xF000 == 0x8000):
           
           #Op code: 8xy0 stores value of v[y] into v[x]
           if(self.opcode & 0xF00F == 0x8000):
               self.v[x] = self.v[y]
           
            #Op code: 8xy1 stores value of bitwise OR for v[x] and v[y] into v[x]
           elif(self.opcode & 0xF00F == 0x8001):
               self.v[x] = self.v[x] | self.v[y]
           
            #Op code: 8xy2 stores value of bitwise AND for v[x] and v[y] into v[x]
           elif(self.opcode & 0xF00F == 0x8002):
               self.v[x] = self.v[x] & self.v[y]
           
            #Op code: 8xy3 stores value of bitwise XOR for v[x] and v[y] into v[x]
           elif(self.opcode & 0xF00F == 0x8003):
               self.v[x] = self.v[x] ^ self.v[y]
           
            #Op code: 8xy4 stores value of v[x] +v[y] and sets v[F] to one if v[x] >255
           elif(self.opcode & 0xF00F == 0x8004):
              result = self.v[x] + self.v[y]
              if(result > 255):
                  self.v[x] = result - 256
                  self.v[0xF]= 1
              else:
                  self.v[x] = result
                  self.v[0xF]= 0
           
            #Op code: 8xy5 stores value v[x]- v[y]
           elif(self.opcode & 0xF00F == 0x8005):
              if( self.v[x] > self.v[y]):
                  self.v[x] -= self.v[y]
                  self.v[0xF]= 1
              else:
                  self.v[x] = 256 + self.v[x] - self.v[y]
                  self.v[0xF]=0
            #Op code: 8xy6 Store the value of register VY shifted left one bit in register VX
            # Set v[f] to the most sig bit prior to shift
           elif(self.opcode & 0xF00F == 0x8006):
              self.v[0xF] = self.v[x] & 1
              self.v[x] = self.v[y] >> 1
            #Op code: 8xy7 if v[y] > v[x] then v[f] is set to 1 otherwise 0 then 
            #store the result of v[x]-v[y] in v[x] 
           elif(self.opcode & 0xF00F == 0x8007):
               if(self.v[y] > self.v[x]):
                   self.v[0xF] = 1
               else:
                   self.v[0xF] = 0
               self.v[x] = self.v[y] - self.v[x] 
           
            #Op code: 8xyE find the most sig bit is 1 then v[f] is set to 1 
            #otherwise v[f] = 0, then v[x] is multiplied by 2   
           elif(self.opcode & 0xF00F == 0x800E):
               self.v[0xF] = (self.v[x] >> 8) 
               self.v[x] = (self.v[y] << 1)
       
        #Op code: 9xy0 checks if v[x] and v[y] are equal if not skips next 
        #instruction by increasing pc by 2
       elif(self.opcode & 0xF000 == 0x9000):
           if(self.v[x] != self.v[y]):
               self.pc +=2
       
        #Op code: Annn The value of register I is set to nnn
       elif(self.opcode & 0xF000 == 0xA000):
           self.idx = (self.opcode & 0x0FFF)
           print(self.idx)
        #Op code: Bnnn jumps to location nnn + v[0]
       elif(self.opcode & 0xF000 == 0xB000):
           self.pc = (self.opcode & 0x0FFF) + self.v[0]
           self.pc -= 2
        #Op code: Cxkk randomly generates number then bitwise AND 
        #it with kk and store it in v[x]
       elif(self.opcode & 0xF000 == 0xC000):
           rand = randint(0,255)
           self.v[x] = rand & kk
       
        #Op code: Dxyn display n-byte sprite starting 
        #at memory location idx at (v[x], v[y]) 
        
       elif(self.opcode & 0xF000 == 0xD000):
           xcord = self.v[x]
           ycord = self.v[y]
           height = self.opcode & 0x000F
           pixel = 0
           self.v[0xF] = 0
           
           for y in range(height):
               pixel = self.memory[self.idx + y]
               for x in range(8):
                   i = xcord + x + ((y + ycord) * 64)
                   if pixel & (0x80 >> x) != 0 and not (y + ycord >= 32 or x + xcord >= 64):
                       if self.gfx[i] == 1:
                           self.v[0xF] = 1
                       self.gfx[i] ^= 1    
           self.draw_flag = True
       #Op codes starting with E
       elif(self.opcode & 0xF000 == 0xE000):
           keys_pressed = key.get_pressed()
           #Opcode: Ex9E skips next instruction if key with value of v[x] is pressed
           if(self.opcode & 0xF0FF == 0xE09E):
               if keys_pressed[main.KEY_MAP[self.v[x]]]:
                    self.pc += 2
                 
           #Op code: ExA1 skips next instruction if key with the value of v[x] is not pressed
           if(self.opcode & 0xF0FF == 0xE0A1):
               if not keys_pressed[main.KEY_MAP[self.v[x]]]:
                   self.pc += 2
       
       #Op codes starting with F
       elif(self.opcode & 0xF000 == 0xF000):
           
           #Opcode: Fx07 places value of delay timer into v[x]
           if(self.opcode & 0xF0FF == 0xF007):
               self.v[x] = self.delay_timer
           
           #Opcode: Fx0A waits for key press stores value of key in v[x] 
           elif(self.opcode & 0xF0FF == 0xF00A):
               pressed = False
               while not pressed:
                   event = pygame.event.wait()
                   if event.type == pygame.KEYDOWN:
                       keys_pressed = key.get_pressed()
                       for keyval, lookup_key in main.KEY_MAP.items():
                           if keys_pressed[lookup_key]:
                               self.v[x] = keyval
                               pressed = True
                               break
           #Opcode: Fx15 sets delay timer = to v[x]
           elif(self.opcode & 0xF0FF == 0xF015):
               self.delay_timer = self.v[x]
           
           #Opcode: Fx18 set sound timer = to v[x] 
           elif(self.opcode & 0xF0FF == 0xF018):
               self.sound_timer = self.v[x]
           
           #Opcode: Fx1E add v[x] to register I
           elif(self.opcode & 0xF0FF == 0xF01E):
               self.idx += self.v[x]
           
           #Opcode: Fx29 set I to the memory address of the sprite data 
           #corresponding to the hexadecimal digit stored in register v[x]
           elif(self.opcode & 0xF0FF == 0xF029):
               self.idx = self.v[x] * 5
           
           #Opcode: Fx33 store binary decimal equivalent of value stored in v[x] at addresses idx, idx+1 and idx+2
           elif(self.opcode & 0xF0FF == 0xF033):
               self.memory[self.idx] = self.v[x] // 100
               self.memory[self.idx + 1] = (self.v[x] //10) % 10
               self.memory[self.idx + 2] = self.v[x] % 10
           
           #Opcode: Fx55 stores values of v[0] + v[x] in memory starting at idx
           elif(self.opcode & 0xF0FF == 0xF055):
               for i in range(x + 1):
                   print(i, self.memory[self.idx + i])
                   self.memory[self.idx + i] = self.v[i]
               self.idx = self.idx + x + 1
           #Fills v[0] to v[x] with values stored in memory starting at idx 
           elif(self.opcode & 0xF0FF == 0xF065):
               for i in range(x + 1):
                   self.v[i] = self.memory[self.idx + i]
                   print(i,':',self.v[i])
               self.idx = self.idx  + x + 1
       else:
           print(self.opcode)
           self.pc -= 2
       
       self.pc += 2 
       
       pytime = time.time()
       if pytime - self.t_last >= 1/600:
           self.update_timers()
           self.t_last =pytime
           