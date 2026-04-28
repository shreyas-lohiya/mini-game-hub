import numpy as np
import pygame
from game import Game

b_height            = 8
b_width             = 8
grid_width          = 1
grid_color          = (0,100,50)
grid_border_color   = (0,40,0)
earthquake          = True
flip_animate_time   = 0.2
fps                 = 60

class Othello(Game):
    def __init__(self,p1,p2,screen,theme):
        self.cell_size_original = 70
        super().__init__(p1,p2,b_height,b_width,screen,theme)
        self.board[self.r//2][self.c//2]=1
        self.board[self.r//2-1][self.c//2-1]=1
        self.board[self.r//2][self.c//2-1]=0
        self.board[self.r//2-1][self.c//2]=0
        self.needtoflip=[]
        self.last_move_time=0
        pygame.display.set_caption("OTHELLO")
    def switch_turn(self):
        self.turn=1-self.turn
        for i in range(self.r):
            for j in range(self.c):
                if self.valid_check(i,j):
                    return True
        self.turn=1-self.turn
        for i in range(self.r):
            for j in range(self.c):
                if self.valid_check(i,j):
                    return True
        return False
    def win_check(self):
        whites = np.sum(self.board==1)
        blacks = np.sum(self.board==0)
        if blacks>whites:
            return self.p1
        elif whites>blacks:
            return self.p2
        else:
            return self.draw_check()
    def draw_check(self):
        return "DRW"
    def outflank_dirn(self,row,col,dirn,mode='check'):
        if dirn[0]==0:
            indicer=self.r
        elif dirn[0]==1:
            indicer=self.r-row
        else:
            indicer=row+1
        if dirn[1]==0:
            indicec=self.c
        elif dirn[1]==1:
            indicec=self.c-col
        else:
            indicec=col+1
        indices=np.arange(1,min(indicer,indicec))
        line=self.board[row+dirn[0]*indices,col+dirn[1]*indices]
        wher=np.where(line!=1-self.turn)[0]
        if wher.size > 0:
            if wher[0]==0:
                return False
            else:
                if line[wher[0]]==self.turn:
                    if mode=='do':
                        indices=1+np.arange(wher[0])
                        for ind in indices:
                            self.needtoflip.append((row+dirn[0]*ind,col+dirn[1]*ind))
                            self.board[row+dirn[0]*ind,col+dirn[1]*ind]=1-self.board[row+dirn[0]*ind,col+dirn[1]*ind]
                    return True
                else:
                    return False
        else:
            return False
    def valid_check(self,row,col):
        if row<0 or col<0 or row >= self.r or col >=self.c or self.board[row][col]!=-1:
            return False
        elif self.outflank_dirn(row,col,(-1,-1)):
            return True
        elif self.outflank_dirn(row,col,(-1,0)):
            return True
        elif self.outflank_dirn(row,col,(-1,1)):
            return True
        elif self.outflank_dirn(row,col,(0,-1)):
            return True
        elif self.outflank_dirn(row,col,(0,1)):
            return True
        elif self.outflank_dirn(row,col,(1,-1)):
            return True
        elif self.outflank_dirn(row,col,(1,0)):
            return True
        elif self.outflank_dirn(row,col,(1,1)):
            return True
        else:
            return False
    def move(self,row,col):
        self.board[row,col]=self.turn
        self.needtoflip=[]
        self.outflank_dirn(row,col,(-1,-1),'do')
        self.outflank_dirn(row,col,(-1,0),'do')
        self.outflank_dirn(row,col,(-1,1),'do')
        self.outflank_dirn(row,col,(0,-1),'do')
        self.outflank_dirn(row,col,(0,1),'do')
        self.outflank_dirn(row,col,(1,-1),'do')
        self.outflank_dirn(row,col,(1,0),'do')
        self.outflank_dirn(row,col,(1,1),'do')
        self.last_move_time=pygame.time.get_ticks()/1000
    def drawboard(self):
        #mean_pos = self.base_pos
        '''
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] :
                mean_pos.y -= 300 * dt
            if keys[pygame.K_s] :
                mean_pos.y += 300 * dt
            if keys[pygame.K_a] :
                mean_pos.x -= 300 * dt
            if keys[pygame.K_d] :
                mean_pos.x += 300 * dt
            if self.earthquake :
                randx=2*np.random.rand()-1
                randy=2*np.random.rand()-1
                self.base_pos.x = mean_pos.x + 600 * dt * randx
                self.base_pos.y = mean_pos.y + 600 * dt * randy
            '''
            
        chip_radius=20*min(self.screen.get_width()/1280, self.screen.get_height()/720)
        t=pygame.time.get_ticks()/1000-self.last_move_time
        if t>flip_animate_time:
            self.needtoflip=[]
        pygame.draw.rect(self.screen,grid_color,(self.base_pos.x-grid_width,self.base_pos.y-grid_width,self.cell_size*self.c+2*grid_width,self.cell_size*self.r+2*grid_width),width=0,border_radius=grid_width)
        pygame.draw.rect(self.screen,grid_border_color,(self.base_pos.x-grid_width,self.base_pos.y-grid_width,self.cell_size*self.c+2*grid_width,self.cell_size*self.r+2*grid_width),width=grid_width,border_radius=grid_width)
        for i in range(self.r):
            for j in range(self.c):
                pygame.draw.rect(self.screen,grid_border_color,(self.base_pos.x+j*self.cell_size,self.base_pos.y+i*self.cell_size,self.cell_size,self.cell_size),width=grid_width)
                if (i,j) in self.needtoflip:
                    new_color = (255*(1-self.turn),255*(1-self.turn),255*(1-self.turn))
                    old_color = (255*self.turn,255*self.turn,255*self.turn)
                    angle=np.pi*(t/flip_animate_time)
                    if angle<np.pi:
                        height=abs(2*chip_radius*np.cos(angle)) 
                        surface = pygame.Surface((2*chip_radius, 2*chip_radius))
                        surface.fill(grid_color)
                        pygame.draw.ellipse(surface, new_color if angle>np.pi/2 else old_color,(0,chip_radius-height/2,2*chip_radius,height))
                        surface2 = pygame.transform.rotate(surface, 30)
                        rect = surface2.get_rect(center=(self.base_pos.x+j*self.cell_size+self.cell_size/2,self.base_pos.y+i*self.cell_size+self.cell_size/2))
                        self.screen.blit(surface2, rect)
                elif self.board[i,j]==0:
                    pygame.draw.circle(self.screen,"black",(self.base_pos.x+j*self.cell_size+self.cell_size/2,self.base_pos.y+i*self.cell_size+self.cell_size/2),chip_radius)
                elif self.board[i,j]==1:
                    pygame.draw.circle(self.screen,"white",(self.base_pos.x+j*self.cell_size+self.cell_size/2,self.base_pos.y+i*self.cell_size+self.cell_size/2),chip_radius)
        pygame.draw.circle(self.screen,(255*self.turn,255*self.turn,255*self.turn),pygame.mouse.get_pos(),chip_radius)
        j=int((pygame.mouse.get_pos()[0]-self.base_pos.x)//self.cell_size)
        i=int((pygame.mouse.get_pos()[1]-self.base_pos.y)//self.cell_size)
        if i>=0 and i<self.r and j>=0 and j<self.c:
            if self.valid_check(i,j):
                pygame.draw.rect(self.screen,"cyan",(self.base_pos.x+j*self.cell_size,self.base_pos.y+i*self.cell_size,self.cell_size,self.cell_size),width=grid_width)
            else:
                pygame.draw.rect(self.screen,"red",(self.base_pos.x+j*self.cell_size,self.base_pos.y+i*self.cell_size,self.cell_size,self.cell_size),width=grid_width)
    def specificmousepressevents(self,eventpos):
        j=int((eventpos[0]-self.base_pos.x)//self.cell_size)
        i=int((eventpos[1]-self.base_pos.y)//self.cell_size)
        if self.valid_check(i,j):
            self.move(i,j)
            if not self.switch_turn():
                self.result = self.win_check()
                self.resultscreen=True