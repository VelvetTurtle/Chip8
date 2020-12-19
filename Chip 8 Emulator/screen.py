# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 15:30:37 2020

@author: velve
"""
from pygame import display, draw, Rect
class Screen(object):
    
    def __init__(self, scale, c8):
        self.c8 = c8     
        self.height = 32  
        self.width = 64
        self.scale = scale 
        self.surface = None
        black = 0,0,0
        white = 255,255,255
        self.colors = [black, white]
    
    #creates a new surface using pygame of width 64 * scale and height 32 * scale
    def initiate_display(self):
        self.surface = display.set_mode(((self.width * self.scale),
        (self.height * self.scale)))
        display.set_caption("Vip8")
        self.clear_screen()
        self.update_screen()
    
    #clears screen by making all the pixels black
    def clear_screen(self):
        self.surface.fill(self.colors[0])
    def update_screen(self):
        display.update()
    
    #draws a rectangle sprite at the location set by dxyn function
    def draw_sprite(self, chip8):
        for x in range(self.width):
            for y in range(self.height):
                self.surface.fill(self.colors[self.c8.gfx[x + (y * self.width)]], Rect(x*self.scale, y*self.scale, self.scale, self.scale))
    #closes the window 
    def destroy(self):
        display.quit()           