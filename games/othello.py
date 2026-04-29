import numpy as np
import pygame
from games.game_template import Game

b_height            = 8
b_width             = 8
grid_width          = 1
grid_color          = (0,100,50)
grid_border_color   = (0,40,0)
flip_animate_time   = 0.2
fps                 = 60

class Othello(Game):
    #sets up intial board and an array containing elements that need to get animated, the last time animation was called, along with caption
    def __init__(self,p1,p2,screen,theme,boardshaking):
        super().__init__(p1,p2,b_height,b_width,70,20,screen,theme,boardshaking)
        self.board[self.r//2-1][self.c//2-1]=1
        self.board[self.r//2][self.c//2-1]=0
        self.board[self.r//2-1][self.c//2]=0
        self.board[self.r//2][self.c//2]=1
        self.needtoflip=[]
        self.last_animate_time=0
        pygame.display.set_caption("OTHELLO")
        
    #switch turn overrideen to include the fact that othello switches turn if the other player has no valid moves,
    #and if both do not have a valid move game ends,
    #swithc turn shows this by returing false if both dont have a valid turn or else true
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
    
    #checks win condition which is just who has more number of chips
    def win_check(self):
        blacks = np.sum(self.board==0)
        whites = np.sum(self.board==1)
        if blacks>whites:
            return self.p1
        elif whites>blacks:
            return self.p2
        else:
            return self.draw_check()
        
    #if draw is ever called it would have been after the game ends and no one wins, so always a draw
    def draw_check(self):
        return "DRW"
    
    #checks direction for outflanking also optionally flips the tokens if mode is 'do'
    #indice_r is the number of steps we can move in the row direction depending on dirn and current row
    #similarly indice_c is the number of steps we can move in the column direction depending on dirn and current col
    #indices stores the steps from 1 till the maximum possible steps in that direction within the board
    #line stores the values of the cells along the given direction starting from (row,col)
    #wher stores the indices where the value is not equal to the opponent's token (1-self.turn)
    #if wher has some values then we check the first such index
    #if the first index itself is 0 it means the adjacent cell is not opponent so no outflank possible
    #otherwise if the value at that position is equal to self.turn then outflanking condition is satisfied
    #if mode is 'do' then we flip all the tokens from 1 till that index and also store them in needtoflip for animation
    #if the value is not self.turn then outflank is not possible
    #if wher is empty it means all tokens in that direction are opponent so no outflank possible
    def outflank_dirn(self,row,col,dirn,mode='check'):
        if dirn[0]==0:
            indice_r=self.r
        elif dirn[0]==1:
            indice_r=self.r-row
        else:
            indice_r=row+1
        if dirn[1]==0:
            indice_c=self.c
        elif dirn[1]==1:
            indice_c=self.c-col
        else:
            indice_c=col+1
        indices=np.arange(1,min(indice_r,indice_c))
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
        
    #simply checks over all the 8 directions
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
        
    #empties whatever chips were being shown in flipping animation
    #places a chip on board
    #then does outflank over all the 8  directins
    #sets last animation time
    def move(self,row,col):
        self.needtoflip=[]
        self.board[row,col]=self.turn
        self.outflank_dirn(row,col,(-1,-1),'do')
        self.outflank_dirn(row,col,(-1,0),'do')
        self.outflank_dirn(row,col,(-1,1),'do')
        self.outflank_dirn(row,col,(0,-1),'do')
        self.outflank_dirn(row,col,(0,1),'do')
        self.outflank_dirn(row,col,(1,-1),'do')
        self.outflank_dirn(row,col,(1,0),'do')
        self.outflank_dirn(row,col,(1,1),'do')
        self.last_animate_time=pygame.time.get_ticks()/1000
        
    #given the time since last flip, and position of chip, it calcuates and displays how the chip would look at certain angle on that t
    def flipanimate(self,t,i,j):
        new_color = (255*(1-self.turn),255*(1-self.turn),255*(1-self.turn))
        old_color = (255*self.turn,255*self.turn,255*self.turn)
        angle=np.pi*(t/flip_animate_time)
        if angle<np.pi:
            height=abs(2*self.piece_radius*np.cos(angle)) 
            surface = pygame.Surface((2*self.piece_radius, 2*self.piece_radius))
            surface.fill(grid_color)
            pygame.draw.ellipse(surface, new_color if angle>np.pi/2 else old_color,(0,self.piece_radius-height/2,2*self.piece_radius,height))
            surface2 = pygame.transform.rotate(surface, 30)
            rect = surface2.get_rect(center=(self.base_pos.x+j*self.cell_size+self.cell_size/2,self.base_pos.y+i*self.cell_size+self.cell_size/2))
            self.screen.blit(surface2, rect)
            
    #draws board along with animation and colors to indicate if there is a valid move there or not
    def drawboard(self):
        t=pygame.time.get_ticks()/1000-self.last_animate_time
        if t>flip_animate_time:
            self.needtoflip=[]
        pygame.draw.rect(self.screen,grid_color,(self.base_pos.x-grid_width,self.base_pos.y-grid_width,self.cell_size*self.c+2*grid_width,self.cell_size*self.r+2*grid_width),width=0,border_radius=grid_width)
        pygame.draw.rect(self.screen,grid_border_color,(self.base_pos.x-grid_width,self.base_pos.y-grid_width,self.cell_size*self.c+2*grid_width,self.cell_size*self.r+2*grid_width),width=grid_width,border_radius=grid_width)
        for i in range(self.r):
            for j in range(self.c):
                pygame.draw.rect(self.screen,grid_border_color,(self.base_pos.x+j*self.cell_size,self.base_pos.y+i*self.cell_size,self.cell_size,self.cell_size),width=grid_width)
                if (i,j) in self.needtoflip:
                    self.flipanimate(t,i,j)
                elif self.board[i,j]==0:
                    pygame.draw.circle(self.screen,"black",(self.base_pos.x+j*self.cell_size+self.cell_size/2,self.base_pos.y+i*self.cell_size+self.cell_size/2),self.piece_radius)
                elif self.board[i,j]==1:
                    pygame.draw.circle(self.screen,"white",(self.base_pos.x+j*self.cell_size+self.cell_size/2,self.base_pos.y+i*self.cell_size+self.cell_size/2),self.piece_radius)
        pygame.draw.circle(self.screen,(255*self.turn,255*self.turn,255*self.turn),pygame.mouse.get_pos(),self.piece_radius)
        j=int((pygame.mouse.get_pos()[0]-self.base_pos.x)//self.cell_size)
        i=int((pygame.mouse.get_pos()[1]-self.base_pos.y)//self.cell_size)
        if i>=0 and i<self.r and j>=0 and j<self.c:
            if self.valid_check(i,j):
                pygame.draw.rect(self.screen,"cyan",(self.base_pos.x+j*self.cell_size,self.base_pos.y+i*self.cell_size,self.cell_size,self.cell_size),width=grid_width)
            else:
                pygame.draw.rect(self.screen,"red",(self.base_pos.x+j*self.cell_size,self.base_pos.y+i*self.cell_size,self.cell_size,self.cell_size),width=grid_width)
                
    #calculates which cell is trying to get placed upon, sees validity, then through switch turn after moving it knows if game has ended or not
    def specificmousepressevents(self,eventpos):
        j=int((eventpos[0]-self.base_pos.x)//self.cell_size)
        i=int((eventpos[1]-self.base_pos.y)//self.cell_size)
        if self.valid_check(i,j):
            self.move(i,j)
            if not self.switch_turn():
                self.result = self.win_check()
                self.resultscreen=True