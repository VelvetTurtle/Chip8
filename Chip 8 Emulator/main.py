# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 14:31:30 2020

@author: velve
"""
import screen
import chip8
import pygame, os, tkinter, sys
from tkinter import filedialog, messagebox

pygame.init

KEY_MAP = {
    0x1: pygame.K_1,
    0x2: pygame.K_2,
    0x3: pygame.K_3,
    0xC: pygame.K_4,
    0x4: pygame.K_q,
    0x5: pygame.K_w,
    0x6: pygame.K_e,
    0xD: pygame.K_r,
    0x7: pygame.K_a,
    0x8: pygame.K_s,
    0x9: pygame.K_d,
    0xE: pygame.K_f,
    0xA: pygame.K_z,
    0x0: pygame.K_x,
    0xB: pygame.K_c,
    0xF: pygame.K_v}

scale = 10

def game_loop():
        
    # create chip8 object
    c8 = chip8.Chip8()
    
    #create a tkinter window
    root = tkinter.Tk()
    
    #Create a window that will ask the user to select the rom they
    #would like to use
    file_name = filedialog.askopenfilename(
        initialdir = os.getcwd(),
        filetypes = (("Chip-8 ROMs *.ch8","*.ch8"), ("Chip-8 ROMS *.c8","*.c8")),
        title = 'Select Game')
    
    #Error message if no rom is detected
    if file_name == '':
        messagebox.showinfo('', 'Error: No ROM selected')
        root.destroy()
        return
    root.destroy()
    
    #Create new screen object
    scr = screen.Screen(scale, c8)
    #initiate that object's display
    scr.initiate_display()
    
    c8.load_rom(file_name)

    running = True
    while running:
        #sends opcode from rom to be decoded and run
        c8.emulate_cycle(scr)
        
        #if last opcode was Dxyn call draw_sprite and update screen
        if c8.draw_flag == True:
            scr.draw_sprite(chip8)
            scr.update_screen()
            c8.draw_flag = False
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                key_pressed = pygame.key.get_pressed()
                if key_pressed[pygame.K_ESCAPE]:
                    running = False
    scr.destroy()
            
if __name__ == "__main__":
    game_loop()