import numpy as np
import pygame

from game import Game

fps=60 
line_color = (200,200,200)
grid_width=1
tplen=0.005
buffer_time = 0.5

class TicTacToe(Game):

    def __init__(self,p1,p2,screen,theme):
        self.cell_size_original=60
        super().__init__(p1,p2,10,10,screen,theme)
        pygame.display.set_caption("Tic-Tac-Toe")  
        self.x_img=pygame.image.load("images/x.png")
        self.o_img=pygame.image.load("images/o.png")
        self.x_img.set_colorkey((0,0,18))
        self.o_img.set_colorkey((0,0,18))
        self.win_animation_active=False

    def dirn(self,i,j,k,dirn):
        indice = np.arange(0,k)
        x_1 = i+dirn[0]*indice
        y_1 = j+dirn[1]*indice
        x_2 = i-dirn[0]*indice
        y_2 = j-dirn[1]*indice
        mask_1 = (x_1>=0)&(x_1<self.r)&(y_1>=0)&(y_1<self.c)
        mask_2 = (x_2>=0)&(x_2<self.r)&(y_2>=0)&(y_2<self.c)
        line_1 = np.where(self.board[x_1[mask_1], y_1[mask_1]]==self.turn,1,0)
        line_2 = np.where(self.board[x_2[mask_2], y_2[mask_2]]==self.turn,1,0)
        s_1=np.where(line_1==0)[0]
        s_2=np.where(line_2==0)[0]
        k_1=s_1[0]-1 if s_1.size>0 else line_1.size - 1
        k_2=s_2[0]-1 if s_2.size>0 else line_2.size - 1
        if(k_1+k_2+1>=k):
            self.end_1 = (i + dirn[0] * k_1, j + dirn[1] * k_1)
            self.end_2 = (i - dirn[0] * k_2, j - dirn[1] * k_2)
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
        return np.all(self.board!=-1)
        
    def valid_check(self,i,j):
        return self.board[i][j]==-1
    
    def move(self,i,j):
        self.board[i][j]=self.turn

    def drawline(self):
        if not self.win_animation_active:
            return

        s_row, s_col = self.end_1
        e_row, e_col = self.end_2
        
        strt = np.array([
            self.base_pos.x + s_col * self.cell_size + self.cell_size // 2, 
            self.base_pos.y + s_row * self.cell_size + self.cell_size // 2])
        
        edn = np.array([
            self.base_pos.x + e_col * self.cell_size + self.cell_size // 2, 
            self.base_pos.y + e_row * self.cell_size + self.cell_size // 2])

        dist = np.linalg.norm(edn - strt)
        draw_duration = tplen * dist
        
        current_time = pygame.time.get_ticks() / 1000.0
        t = current_time - self.win_animation_start

        progress = min(1.0, t / draw_duration) if draw_duration > 0 else 1.0
        current_tip = strt + (edn - strt) * progress

        temp_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        alpha = int(50 + (100 *((np.sin(pygame.time.get_ticks() / 150) + 1) / 2)))
        pygame.draw.line(temp_surface, (0, 120, 255,alpha), strt, current_tip, width=15)
        self.screen.blit(temp_surface, (0, 0))

        if t >= draw_duration + buffer_time:
            pygame.draw.line(temp_surface, (0, 120, 255,0), strt, current_tip, width=15)
            self.screen.blit(temp_surface, (0, 0))
            self.win_animation_active = False
            self.result = self.p1 if self.turn == 0 else self.p2
            self.resultscreen = True
    
    def drawboard(self):
        self.x_resized_img = pygame.transform.scale(self.x_img,(self.cell_size-2,self.cell_size-2))
        self.o_resized_img = pygame.transform.scale(self.o_img,(self.cell_size-2,self.cell_size-2))
        for i in range(self.r):
            for j in range(self.c):
                rect = pygame.draw.rect(self.screen,line_color,(self.base_pos.x+j*self.cell_size,self.base_pos.y+i*self.cell_size,self.cell_size,self.cell_size),width=grid_width)
                if self.board[i][j] == 0:
                    self.screen.blit(self.x_resized_img,(rect.left+1,rect.top+1))
                elif self.board[i][j] == 1:
                    self.screen.blit(self.o_resized_img,(rect.left+1,rect.top+1))
        
        if self.win_animation_active:
            self.drawline()

    def specificmousepressevents(self, eventpos):
        if self.resultscreen or self.win_animation_active:
            return
        
        j=int((eventpos[0]-self.base_pos.x)//self.cell_size)
        i=int((eventpos[1]-self.base_pos.y)//self.cell_size)
        if self.valid_check(i,j) :
            self.move(i,j)
            if self.win_check(i,j):
                self.win_animation_active = True
                self.win_animation_start = pygame.time.get_ticks() / 1000.0
            elif self.draw_check():
                self.result = "DRW"
                self.resultscreen = True
            else:
                self.switch_turn()