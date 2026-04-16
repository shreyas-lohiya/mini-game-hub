import sys
import os
import numpy
import pygame

from game import Game

class Connect4(Game):

    def __init__(self,p1,p2,screen):
        self.p1=p1
        self.p2=p2
        super().__init__(p1,p2,7,7,screen)
    
    def dirn(self,i,j,k,dirn):
        indice = numpy.arange(-k+1,k)
        x = i+dirn[0]*indice
        y = j+dirn[1]*indice
        mask = (x>=0)&(x<self.r)&(y>=0)&(y<self.c)
        line = self.board[x[mask], y[mask]]
        fin = numpy.where(line==self.turn,1,0)
        if numpy.any(numpy.convolve(fin,numpy.ones(k),'valid')==k):
            return True
        else:
            return False
        
    def win_check(self,i,j,k=4):
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
        
    def valid_check(self,j):
        return self.board[0][j]==-1 
    
    def move(self,j):
        i=self.r-1
        while i>=0 and self.board[i][j]!=-1 :
            i=i-1
        self.board[i][j]=self.turn
        return i

    def play(self):
        res = (1280,720)
        bg_color = (0,0,18)
        line_color = (200,200,200)
        pygame.display.set_caption("Connect4")

        cells = []
        cell_w = int(560/self.c)
        cell_h = int(560/self.r)

        for x in range(self.r):
            for y in range(self.c):
                left=360+y*cell_w
                top=80+x*cell_h
                rect=pygame.Rect(left,top,cell_w,cell_h)
                cells.append(rect)
        
        token1_img=pygame.image.load("images/token1.png")
        t1_img = pygame.transform.scale(token1_img,(cell_w-2,cell_h-2))
        token2_img=pygame.image.load("images/token2.png")
        t2_img = pygame.transform.scale(token2_img,(cell_w-2,cell_h-2))

        while True:
            self.screen.fill(bg_color)
            for rect in cells:
                pygame.draw.rect(self.screen,line_color,rect,1) 
            mouse_pos = pygame.mouse.get_pos()
            for i in range(self.r):
                for j in range(self.c):
                    if self.board[i][j] == 0:
                        rect = cells[i*self.c+j]
                        self.screen.blit(t1_img,(rect.left+1,rect.top+1))
                    if self.board[i][j] == 1:
                        rect = cells[i*self.c + j]
                        self.screen.blit(t2_img,(rect.left+1,rect.top+1))
                    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x = event.pos[0]
                        j = int((x - 360) // cell_w)
                        if 0 <= j < self.c and self.valid_check(j):
                            i = self.move(j)
                            if self.win_check(i,j):
                                if self.turn==0:
                                    return self.p1
                                else:
                                    return self.p2
                            self.switch_turn()
                            if self.draw_check():
                                return "DRW"
            pygame.display.flip()
    
    

        
    

