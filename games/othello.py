import numpy as np
import pygame
from game import Game,Button

grid_size           = 3
grid_unit           = 70
grid_width          = 1
grid_color          = (0,100,50)
grid_border_color   = (0,40,0)
bg_color            = (205,200,200)
chip_radius         = 20
earthquake          = True
flip_animate_time   = 0.2
fps                 = 60

class Othello(Game):
    def __init__(self,p1,p2,screen,theme):
        super().__init__(p1,p2,grid_size,grid_size,screen,theme)
        self.board[grid_size//2][grid_size//2]=1
        self.board[grid_size//2-1][grid_size//2-1]=1
        self.board[grid_size//2][grid_size//2-1]=0
        self.board[grid_size//2-1][grid_size//2]=0
        self.needtoflip=[]
        self.last_move_time=0
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
    def play(self):
        quitscreen=False
        resultscreen=False
        drawclaimed=False
        pygame.display.set_caption("OTHELLO")
        self.base_pos = pygame.Vector2(self.screen.get_width() / 2 - grid_unit*grid_size/2, self.screen.get_height() / 2 - grid_unit*grid_size/2)
        mean_pos = self.base_pos.copy()
        while True:
            t=pygame.time.get_ticks()/1000-self.last_move_time
            if t>flip_animate_time:
                self.needtoflip=[]
            dt = self.clock.tick(fps)/1000
            self.screen.fill(bg_color)
            self.screen.blit(self.bg,(0,0))
            pygame.draw.rect(self.screen,grid_color,(self.base_pos.x-grid_width,self.base_pos.y-grid_width,grid_unit*grid_size+2*grid_width,grid_unit*grid_size+2*grid_width),width=0,border_radius=grid_width)
            pygame.draw.rect(self.screen,grid_border_color,(self.base_pos.x-grid_width,self.base_pos.y-grid_width,grid_unit*grid_size+2*grid_width,grid_unit*grid_size+2*grid_width),width=grid_width,border_radius=grid_width)
            for i in range(grid_size):
                for j in range(grid_size):
                    pygame.draw.rect(self.screen,grid_border_color,(self.base_pos.x+i*grid_unit,self.base_pos.y+j*grid_unit,grid_unit,grid_unit),width=grid_width)
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
                            rect = surface2.get_rect(center=(self.base_pos.x+i*grid_unit+grid_unit/2,self.base_pos.y+j*grid_unit+grid_unit/2))
                            self.screen.blit(surface2, rect)
                    elif self.board[i,j]==0:
                        pygame.draw.circle(self.screen,"black",(self.base_pos.x+i*grid_unit+grid_unit/2,self.base_pos.y+j*grid_unit+grid_unit/2),chip_radius)
                    elif self.board[i,j]==1:
                        pygame.draw.circle(self.screen,"white",(self.base_pos.x+i*grid_unit+grid_unit/2,self.base_pos.y+j*grid_unit+grid_unit/2),chip_radius)

            pygame.draw.circle(self.screen,(255*self.turn,255*self.turn,255*self.turn),pygame.mouse.get_pos(),chip_radius)
            i=int((pygame.mouse.get_pos()[0]-self.base_pos.x)//grid_unit)
            j=int((pygame.mouse.get_pos()[1]-self.base_pos.y)//grid_unit)
            if i>=0 and i<grid_size and j>=0 and j<grid_size:
                if self.valid_check(i,j):
                    pygame.draw.rect(self.screen,"cyan",(self.base_pos.x+i*grid_unit,self.base_pos.y+j*grid_unit,grid_unit,grid_unit),width=grid_width)
                else:
                    pygame.draw.rect(self.screen,"red",(self.base_pos.x+i*grid_unit,self.base_pos.y+j*grid_unit,grid_unit,grid_unit),width=grid_width)

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
                self.base_pos.x = mean_pos.x + 600 * dt * randx
                self.base_pos.y = mean_pos.y + 600 * dt * randy
            player1=self.font.render(f"{self.p1}", True, (200, 200, 200))
            self.screen.blit(player1, player1.get_rect(center=(self.screen.get_width()/2-400,120)))
            player2=self.font.render(f"{self.p2}", True, (200, 200, 200))
            self.screen.blit(player2, player2.get_rect(center=(self.screen.get_width()/2+400,120)))
            self.btnresign1.draw(pygame.mouse.get_pos(),dt,self.screen)
            self.btnresign2.draw(pygame.mouse.get_pos(),dt,self.screen)
            self.btnclaimdraw1.draw(pygame.mouse.get_pos(),dt,self.screen)
            self.btnclaimdraw2.draw(pygame.mouse.get_pos(),dt,self.screen)
            if quitscreen :
                title=self.font.render("You sure you wanna quit ?", True, (200, 200, 200))
                title = pygame.transform.scale_by(title,1+0.05*np.sin(pygame.time.get_ticks()/200))
                self.screen.blit(title, title.get_rect(center=(self.screen.get_width()/2,120)))
                self.btnquityes.draw(pygame.mouse.get_pos(),dt,self.screen)
                self.btnquitno.draw(pygame.mouse.get_pos(),dt,self.screen)
            elif resultscreen :
                if result=="DRW":
                    title=self.font.render("DRAW", True, (200, 200, 200))
                    title = pygame.transform.scale_by(title,1+0.05*np.sin(pygame.time.get_ticks()/200))
                    self.screen.blit(title, title.get_rect(center=(self.screen.get_width()/2,self.screen.get_height()/2)))
                else:
                    title=self.font.render(f"WINNER IS {result}", True, (200, 200, 200))
                    title = pygame.transform.scale_by(title,1+0.05*np.sin(pygame.time.get_ticks()/200))
                    self.screen.blit(title, title.get_rect(center=(self.screen.get_width()/2,self.screen.get_height()/2)))
                self.btnproceedresult.draw(pygame.mouse.get_pos(),dt,self.screen)
            elif drawclaimed:
                title=self.font.render(f"{whoclaimdraw} claimed draw", True, (200, 200, 200))
                title = pygame.transform.scale_by(title,1+0.05*np.sin(pygame.time.get_ticks()/200))
                self.screen.blit(title, title.get_rect(center=(self.screen.get_width()/2,self.screen.get_height()/2)))
                self.btnacceptdraw.draw(pygame.mouse.get_pos(),dt,self.screen)
                self.btnrejectdraw.draw(pygame.mouse.get_pos(),dt,self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quitscreen=True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if quitscreen:
                        if self.btnquityes.pressed(pygame.mouse.get_pos()):
                            return None
                        elif self.btnquitno.pressed(pygame.mouse.get_pos()):
                            quitscreen=False
                    elif resultscreen:
                        if self.btnproceedresult.pressed(pygame.mouse.get_pos()):
                            return result
                    elif drawclaimed:
                        if self.btnacceptdraw.pressed(pygame.mouse.get_pos()):
                            result = "DRW"
                            resultscreen=True
                        elif self.btnrejectdraw.pressed(pygame.mouse.get_pos()):
                            drawclaimed=False
                    elif self.btnresign1.pressed(pygame.mouse.get_pos()):
                        result = self.p2
                        resultscreen = True
                    elif self.btnresign2.pressed(pygame.mouse.get_pos()):
                        result = self.p1
                        resultscreen = True
                    elif self.btnclaimdraw1.pressed(pygame.mouse.get_pos()):
                        whoclaimdraw = self.p1
                        drawclaimed = True
                    elif self.btnclaimdraw2.pressed(pygame.mouse.get_pos()):
                        whoclaimdraw = self.p2
                        drawclaimed = True
                    else:
                        i=int(event.pos[0]-self.base_pos.x)//grid_unit
                        j=int(event.pos[1]-self.base_pos.y)//grid_unit
                        if self.valid_check(i,j):
                            self.move(i,j)
                            if not self.switch_turn():
                                result = self.win_check()
                                resultscreen=True
            pygame.display.flip()
            