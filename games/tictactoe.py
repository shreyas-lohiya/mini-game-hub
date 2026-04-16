import sys
import os
import numpy as np
import pygame

from game import Game

class TicTacToe(Game):

    def __init__(self,p1,p2,screen):
        self.p1=p1
        self.p2=p2
        super().__init__(p1,p2,10,10,screen)

    def dirn(self,i,j,k,dirn):
        indice = np.arange(-k+1,k)
        x = i+dirn[0]*indice
        y = j+dirn[1]*indice
        mask = (x>=0)&(x<self.r)&(y>=0)&(y<self.c)
        line = self.board[x[mask], y[mask]]
        fin = np.where(line==self.turn,1,0)
        if np.any(np.convolve(fin,np.ones(k),'valid')==k):
            return True
        else:
            return False

    def win_check(self,i,j,k=5):
        if self.dirn(i,j,k,[0,1]):
            return True
        elif self.dirn(i,j,k,[1,0]):
            return True
        elif self.dirn(i,j,k,[1,1]):
            return True
        elif self.dirn(i,j,k,[1,-1]):
            return True
        else:
            return False
        
    def draw_check(self):
        if (self.board == -1).sum() == 0:
            return True
        else:
            return False
        
    def valid_check(self,i,j):
        return self.board[i][j]==-1
    
    def move(self,i,j):
        self.board[i][j]=self.turn
            
    def play(self):
        res = (1280,720)
        bg_color = (0,0,18)
        line_color = (200,200,200)
        pygame.display.set_caption("Tic-Tac-Toe")

        cells = []
        cell_w = int(600/self.c)
        cell_h = int(600/self.r)

        for x in range(self.r):
            for y in range(self.c):
                left=340+y*cell_w
                top=60+x*cell_h
                rect=pygame.Rect(left,top,cell_w,cell_h)
                cells.append(rect)
        
        x_img=pygame.image.load("images/x.png")
        x_resized_img = pygame.transform.scale(x_img,(cell_w-2,cell_h-2))
        o_img=pygame.image.load("images/o.png")
        o_resized_img = pygame.transform.scale(o_img,(cell_w-2,cell_h-2))
        x_img.set_colorkey((0,0,18))
        o_img.set_colorkey((0,0,18))
        
    
        while True:
            self.screen.fill(bg_color)
            for rect in cells:
                pygame.draw.rect(self.screen,line_color,rect,1) 
            mouse_pos = pygame.mouse.get_pos()
            for i in range(self.r):
                for j in range(self.c):
                    if self.board[i][j] == 0:
                        rect = cells[i*self.c+j]
                        self.screen.blit(x_resized_img,(rect.left+1,rect.top+1))
                    if self.board[i][j] == 1:
                        rect = cells[i*self.c + j]
                        self.screen.blit(o_resized_img,(rect.left+1,rect.top+1))
                    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for rect in cells:
                        if rect.collidepoint(mouse_pos):
                            i = int((rect.top - 60)//cell_h)
                            j = int((rect.left - 340)//cell_w)
                            if self.valid_check(i,j) :
                                self.move(i,j)
                                if self.win_check(i,j):
                                    if self.turn==0:
                                        return self.p1
                                    else:
                                        return self.p2
                                self.switch_turn()
                                if self.draw_check():
                                    return "DRW"
            pygame.display.flip()

        
