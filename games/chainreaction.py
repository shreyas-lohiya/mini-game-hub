import numpy as np
import pygame
from games.game_template import Game

b_height=9
b_width=6
fps=60
bg_color = (0,0,18)
line_color = (200,200,200)
grid_width = 1 
animate_time = 0.2

class ChainRxn(Game):
    #fills board with zeros, makes a capacity array for easy acess of getting to know which one is at edge or in the middle,
    #sets an array containing elements that need to get animated, the last time animation was called
    def __init__(self,p1,p2,screen,theme):
        super().__init__(p1,p2,b_height,b_width,70,14,screen,theme)
        self.board=np.zeros((b_height,b_width))
        self.capacity=np.zeros((b_height,b_width))
        for i in range(self.r):
            for j in range(self.c):
                if (i==0 or i==self.r-1) and (j==0 or j==self.c-1):
                    self.capacity[i][j]=2
                elif i==0 or i==self.r-1 or j==0 or j==self.c-1:
                    self.capacity[i][j]=3
                else:
                    self.capacity[i][j]=4 
        self.needtoexplode=[]
        self.last_animate_time=0
        pygame.display.set_caption("CHAIN REACTION")
    
    #checks win by checking if the board is full of only one color and that color's total number of balls is>1
    def win_check(self):
        if np.all(self.baord>=0) and np.sum(self.board>0)>1:
            return True
        elif np.all(self.baord<=0) and np.sum(self.board<0)>1:
            return True
        else:
            return False
    
    #checks validity
    def valid_check(self,i,j):
        if i<0 or j<0 or i >= self.r or j >=self.c:
            return False
        elif self.board[i][j]==0:
            return True
        elif (self.board[i][j]>0 and self.turn==0):
            return True
        elif (self.board[i][j]<0 and self.turn==1):
            return True
        else:
            return False
    
    #updates board according to move, and the last time animation started
    def move(self,i,j):
        self.board[i][j] += 1 - 2*self.turn
        self.last_animate_time=pygame.time.get_ticks()/1000
    
    #updatesboard only with the primary explosions, i.e. no secondary explosions are considered
    def updateboard(self):
        self.last_animate_time=pygame.time.get_ticks()/1000
        self.oldboard=self.board.copy()
        for i in range(self.r):
            for j in range(self.c):
                if abs(self.oldboard[i][j])>=self.capacity[i][j]:
                    if i>0:
                        self.board[i-1][j]=(abs(self.board[i-1][j])+1)*np.sign(self.oldboard[i][j])
                    if i<self.r-1:
                        self.board[i+1][j]=(abs(self.board[i+1][j])+1)*np.sign(self.oldboard[i][j])
                    if j>0:
                        self.board[i][j-1]=(abs(self.board[i][j-1])+1)*np.sign(self.oldboard[i][j])
                    if j<self.c-1:
                        self.board[i][j+1]=(abs(self.board[i][j+1])+1)*np.sign(self.oldboard[i][j])
                    self.board[i][j]-=np.sign(self.board[i][j])*self.capacity[i][j]
        #checks win in between this
        if self.win_check():
                if self.turn==0:
                    self.result = self.p1
                else:
                    self.result = self.p2
                self.resultscreen = True
                    
    #draws board along with explosion
    def drawboard(self):
        t=pygame.time.get_ticks()/1000-self.last_animate_time
        if t>animate_time and np.any(abs(self.board)>=self.capacity):
            self.updateboard()
        t=pygame.time.get_ticks()/1000-self.last_animate_time
        for i in range(self.r):
            for j in range(self.c):
                pygame.draw.rect(self.screen,line_color,(self.base_pos.x+j*self.cell_size,self.base_pos.y+i*self.cell_size,self.cell_size,self.cell_size),width=grid_width)
                cx=self.base_pos.x+(j)*self.cell_size+self.cell_size/2
                cy=self.base_pos.y+(i)*self.cell_size+self.cell_size/2
                color = "red" if self.board[i][j]>0 else "green"
                value = abs(self.board[i][j])
                if value>=self.capacity[i][j]:
                    value-=self.capacity[i][j]
                    distance=(self.cell_size-self.piece_radius/2)*(t/animate_time)
                    if i>0:
                        pygame.draw.circle(self.screen,color,(cx,cy-distance),self.piece_radius)
                    if i<self.r-1:
                        pygame.draw.circle(self.screen,color,(cx,cy+distance),self.piece_radius)
                    if j>0:
                        pygame.draw.circle(self.screen,color,(cx-distance,cy),self.piece_radius)
                    if j<self.c-1:
                        pygame.draw.circle(self.screen,color,(cx+distance,cy),self.piece_radius)
                if value>=1:
                    if(value==1):
                        pygame.draw.circle(self.screen,color,(cx,cy),self.piece_radius)
                    elif(value==2):
                        pygame.draw.circle(self.screen,color,(cx-self.piece_radius,cy),self.piece_radius)
                        pygame.draw.circle(self.screen,color,(cx+self.piece_radius,cy),self.piece_radius)
                    elif(value==3):
                        pygame.draw.circle(self.screen,color,(cx,cy-self.piece_radius),self.piece_radius)
                        pygame.draw.circle(self.screen,color,(cx-self.piece_radius,cy+0.75*self.piece_radius),self.piece_radius)
                        pygame.draw.circle(self.screen,color,(cx+self.piece_radius,cy+0.75*self.piece_radius),self.piece_radius)

    #calculates which cell is trying to get placed upon, sees validity,
    #and if the board is stable,
    #then it moves and switches turn
    def specificmousepressevents(self, eventpos):
        j=int((eventpos[0]-self.base_pos.x)//self.cell_size)
        i=int((eventpos[1]-self.base_pos.y)//self.cell_size)
        if self.valid_check(i,j) and np.all(abs(self.board)<self.capacity):
            self.move(i,j)
            self.switch_turn()
    


    
