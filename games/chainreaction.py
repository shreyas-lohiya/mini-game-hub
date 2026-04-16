import sys
import os
import numpy as np
import pygame

from game import Game

class ChainRxn(Game):

    def __init__(self,p1,p2,screen):
        self.p1=p1
        self.p2=p2
        super().__init__(p1,p2,6,9,screen)
        self.board=np.zeros((6,9))

    def pop(self,i,j):
        if (i==0 or i==self.r-1) and (j==0 or j==self.c-1):
            return 2
        elif i==0 or i==self.r-1 or j==0 or j==self.c-1:
            return 3
        else:
            return 4 
    
    def own(self,i,j):
        if(self.board[i][j]==0):
            return -1
        elif(self.board[i][j]/abs(self.board[i][j])==1):
            return 0
        else:
            return 1
        
    
    def win_check(self):
        b=self.board
        if (np.sum(b[b>0]) == np.sum(b)) and (np.sum(b)!=0) and np.sum(b>0)>1:
            return True
        elif np.sum(b[b<0]) == np.sum(b) and (np.sum(b)!=0) and np.sum(b<0)>1:
            return True
        else:
            return False
    
    def valid_check(self,i,j):
        if self.board[i][j]==0:
            return True
        elif (self.board[i][j]>0 and self.turn==0):
            return True
        elif (self.board[i][j]<0 and self.turn==1):
            return True
        else:
            return False
    
    def move(self,i,j):

        if self.turn==0:
            self.board[i][j]+=1
        if self.turn==1:
            self.board[i][j]-=1

        capacity = self.pop(i, j)

        if abs(self.board[i][j])>=capacity:
            self.board[i][j] = 0
            if i>0:
                self.board[i-1][j]=abs(self.board[i-1][j]) * (1 if self.turn == 0 else -1)
                self.move(i-1,j)
            if i<self.r-1:
                self.board[i+1][j]=abs(self.board[i+1][j]) * (1 if self.turn == 0 else -1)
                self.move(i+1,j)
            if j>0:
                self.board[i][j-1]=abs(self.board[i][j-1]) * (1 if self.turn == 0 else -1)
                self.move(i,j-1)
            if j<self.c-1:
                self.board[i][j+1]=abs(self.board[i][j+1]) * (1 if self.turn == 0 else -1)
                self.move(i,j+1)

    def play(self):
        res = (1280,720)
        bg_color = (0,0,18)
        line_color = (200,200,200)
        pygame.display.set_caption("Chain-Reaction")

        cells = []
        cell_w = int(900/self.c)
        cell_h = int(600/self.r)

        for x in range(self.r):
            for y in range(self.c):
                left=190+y*cell_w
                top=60+x*cell_h
                rect=pygame.Rect(left,top,cell_w,cell_h)
                cells.append(rect)
        
        red1_img=pygame.image.load("images/red1.png")
        red1_resized_img = pygame.transform.scale(red1_img,(cell_w-2,cell_h-2))
        red2_img=pygame.image.load("images/red2.png")
        red2_resized_img = pygame.transform.scale(red2_img,(cell_w-2,cell_h-2))
        red3_img=pygame.image.load("images/red3.png")
        red3_resized_img = pygame.transform.scale(red3_img,(cell_w-2,cell_h-2))
        green1_img=pygame.image.load("images/green1.png")
        green1_resized_img = pygame.transform.scale(green1_img,(cell_w-2,cell_h-2))
        green2_img=pygame.image.load("images/green2.png")
        green2_resized_img = pygame.transform.scale(green2_img,(cell_w-2,cell_h-2))
        green3_img=pygame.image.load("images/green3.png")
        green3_resized_img = pygame.transform.scale(green3_img,(cell_w-2,cell_h-2))
        
        while True:
            self.screen.fill(bg_color)
            for rect in cells:
                pygame.draw.rect(self.screen,line_color,rect,1) 
            mouse_pos = pygame.mouse.get_pos()
            for i in range(self.r):
                for j in range(self.c):
                    if self.board[i][j] == 1:
                        rect = cells[i*self.c + j]
                        self.screen.blit(red1_resized_img,(rect.left+1,rect.top+1))
                    if self.board[i][j] == 2:
                        rect = cells[i*self.c + j]
                        self.screen.blit(red2_resized_img,(rect.left+1,rect.top+1))
                    if self.board[i][j] == 3:
                        rect = cells[i*self.c + j]
                        self.screen.blit(red3_resized_img,(rect.left+1,rect.top+1))
                    if self.board[i][j] == -1:
                        rect = cells[i*self.c + j]
                        self.screen.blit(green1_resized_img,(rect.left+1,rect.top+1))
                    if self.board[i][j] == -2:
                        rect = cells[i*self.c + j]
                        self.screen.blit(green2_resized_img,(rect.left+1,rect.top+1))
                    if self.board[i][j] == -3:
                        rect = cells[i*self.c + j]
                        self.screen.blit(green3_resized_img,(rect.left+1,rect.top+1))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for rect in cells:
                        if rect.collidepoint(mouse_pos):
                            i = int((rect.top - 60)//cell_h)
                            j = int((rect.left - 190)//cell_w)
                            if self.valid_check(i,j):
                                self.move(i,j)
                                if self.win_check():
                                    if self.turn==0:
                                        return self.p1
                                    else:
                                        return self.p2
                                self.switch_turn()
            pygame.display.flip()

    


    
