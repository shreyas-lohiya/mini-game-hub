import numpy as np
import pygame
from game import Game

grid_size           = 4
res                 = (1280,720)
grid_unit           = 80
grid_width          = 1
grid_color          = (0,100,50)
grid_border_color   = (0,40,0)
bg_color            = (205,200,200)
chip_radius         = 20
earthquake          = True
flip_animate_time   = 0.25

class Othello(Game):
    def __init__(self,p1,p2):
        super().__init__(p1,p2,grid_size,grid_size)
        self.board[grid_size//2][grid_size//2]=1
        self.board[grid_size//2-1][grid_size//2-1]=1
        self.board[grid_size//2][grid_size//2-1]=0
        self.board[grid_size//2-1][grid_size//2]=0
    def switch_turn(self):
        self.turn=1-self.turn
        for i in range(grid_size):
            for j in range(grid_size):
                if self.valid_check(i,j):
                    return True
        self.turn=1-self.turn
        for i in range(grid_size):
            for j in range(grid_size):
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
    def place_chip(self,row,col):
        self.board[row][col]=self.turn
    def flip_chip(self,row,col):
        t=0
        old_color = (255*(1-self.turn),255*(1-self.turn),255*(1-self.turn))
        new_color = (255*self.turn,255*self.turn,255*self.turn)
        while t<flip_animate_time:
            pygame.draw.rect(screen,grid_color,(base_pos.x+int(row)*grid_unit,base_pos.y+int(col)*grid_unit,grid_unit,grid_unit))
            pygame.draw.rect(screen,grid_border_color,(base_pos.x+int(row)*grid_unit,base_pos.y+int(col)*grid_unit,grid_unit,grid_unit),width=grid_width)
            angle=np.pi*(t/flip_animate_time)
            height=abs(2*chip_radius*np.cos(angle))
            surface = pygame.Surface((2*chip_radius, 2*chip_radius))
            surface.fill(grid_color)
            pygame.draw.ellipse(surface, new_color if angle>np.pi/2 else old_color,(0,chip_radius-height/2,2*chip_radius,height))
            surface2 = pygame.transform.rotate(surface, 30)
            rect = surface2.get_rect(center=(base_pos.x+row*grid_unit+grid_unit/2,base_pos.y+col*grid_unit+grid_unit/2))
            screen.blit(surface2, rect)
            pygame.display.flip()
            t = t+clock.tick(600) / 1000
        self.board[row,col]=1-self.board[row,col]
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
                            self.flip_chip(row+dirn[0]*ind,col+dirn[1]*ind)
                    return True
                else:
                    return False
        else:
            return False
    def valid_check(self,row,col):
        if row<0 or col<0 or row >= grid_size or col >=grid_size or self.board[row][col]!=-1:
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
        self.place_chip(row,col)
        self.outflank_dirn(row,col,(-1,-1),'do')
        self.outflank_dirn(row,col,(-1,0),'do')
        self.outflank_dirn(row,col,(-1,1),'do')
        self.outflank_dirn(row,col,(0,-1),'do')
        self.outflank_dirn(row,col,(0,1),'do')
        self.outflank_dirn(row,col,(1,-1),'do')
        self.outflank_dirn(row,col,(1,0),'do')
        self.outflank_dirn(row,col,(1,1),'do')
    def play(self):
        pygame.init()
        pygame.mixer.music.load("music/Phonk_sample.ogg")
        pygame.mixer.music.play() 
        global screen
        screen = pygame.display.set_mode(size=res)
        bg = pygame.image.load('images/background.png')
        bg = pygame.transform.scale(bg, screen.get_size())
        pygame.display.set_caption("OTHELLO")
        global clock
        clock = pygame.time.Clock()
        dt = 0
        global base_pos
        base_pos = pygame.Vector2(screen.get_width() / 2 - grid_unit*grid_size/2, screen.get_height() / 2 - grid_unit*grid_size/2)
        mean_pos = base_pos.copy()
        running = True
        while running:
            screen.fill(bg_color)
            screen.blit(bg,(0,0))
            pygame.draw.rect(screen,grid_color,(base_pos.x-grid_width,base_pos.y-grid_width,grid_unit*grid_size+2*grid_width,grid_unit*grid_size+2*grid_width),width=0,border_radius=grid_width)
            pygame.draw.rect(screen,grid_border_color,(base_pos.x-grid_width,base_pos.y-grid_width,grid_unit*grid_size+2*grid_width,grid_unit*grid_size+2*grid_width),width=grid_width,border_radius=grid_width)
            for i in range(grid_size):
                for j in range(grid_size):
                    pygame.draw.rect(screen,grid_border_color,(base_pos.x+i*grid_unit,base_pos.y+j*grid_unit,grid_unit,grid_unit),width=grid_width)
                    if self.board[i,j]==0:
                        pygame.draw.circle(screen,"black",(base_pos.x+i*grid_unit+grid_unit/2,base_pos.y+j*grid_unit+grid_unit/2),chip_radius)
                    elif self.board[i,j]==1:
                        pygame.draw.circle(screen,"white",(base_pos.x+i*grid_unit+grid_unit/2,base_pos.y+j*grid_unit+grid_unit/2),chip_radius)

            pygame.draw.circle(screen,(255*self.turn,255*self.turn,255*self.turn),pygame.mouse.get_pos(),chip_radius)
            i=int((pygame.mouse.get_pos()[0]-base_pos.x)//grid_unit)
            j=int((pygame.mouse.get_pos()[1]-base_pos.y)//grid_unit)
            if i>=0 and i<grid_size and j>=0 and j<grid_size:
                if self.valid_check(i,j):
                    pygame.draw.rect(screen,"cyan",(base_pos.x+i*grid_unit,base_pos.y+j*grid_unit,grid_unit,grid_unit),width=grid_width)
                else:
                    pygame.draw.rect(screen,"red",(base_pos.x+i*grid_unit,base_pos.y+j*grid_unit,grid_unit,grid_unit),width=grid_width)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] :
                mean_pos.y -= 300 * dt
            if keys[pygame.K_s] :
                mean_pos.y += 300 * dt
            if keys[pygame.K_a] :
                mean_pos.x -= 300 * dt
            if keys[pygame.K_d] :
                mean_pos.x += 300 * dt
            if earthquake :
                randx=2*np.random.rand()-1
                randy=2*np.random.rand()-1
                base_pos.x = mean_pos.x + 600 * dt * randx
                base_pos.y = mean_pos.y + 600 * dt * randy

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    i=int(event.pos[0]-base_pos.x)//grid_unit
                    j=int(event.pos[1]-base_pos.y)//grid_unit
                    if self.valid_check(i,j):
                        self.move(i,j)
                        if not self.switch_turn():
                            return self.win_check()
            pygame.display.flip()
            dt = clock.tick(6000)/1000
        pygame.quit()