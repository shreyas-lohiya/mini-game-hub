import sys
import os
import numpy
import pygame

from game import Game

class TicTacToe(Game):
    def __init__(self,p1,p2):
        self.p1=p1
        self.p2=p2
        super().__init__(p1,p2,9,9)
    
    def play(self):
        pygame.init()
        res = (1280,720)
        bg_color = (0,0,18)
        line_color = (200,200,200)
        screen = pygame.display.set_mode(res)
        pygame.display.set_caption("Tic-Tac-Toe")

        cells = []
        cell_w = 600/self.c
        cell_h = 600/self.r

        for x in range(self.r):
            for y in range(self.c):
                left=340+y*cell_w
                top=60+x*cell_h
                rect=pygame.Rect(left,top,cell_w,cell_h)
                cells.append(rect)

        while True:
            screen.fill(bg_color)
            for rect in cells:
                pygame.draw.rect(screen,line_color,rect,1) 
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for rect in cells:
                        if rect.collidepoint(mouse_pos):
                            super().switch_turn()

            pygame.display.flip()
