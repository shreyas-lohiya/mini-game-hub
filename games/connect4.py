import numpy as np
import pygame

from game import Game

fps=60
line_color = (200,200,200)
fall_acc=1500
coeff_restitution=0.4
max_bounces=4
speed=800
tplen=0.005
trans_color = (67,67,67)
grid_color = (0,120,255)
buffer_time = 0.5

class Connect4(Game):

    def __init__(self,p1,p2,screen,theme):
        self.cell_size_original=80
        super().__init__(p1,p2,7,7,screen,theme)
        pygame.display.set_caption("Connect4")
        token1_img=pygame.image.load("images/token1.png")
        self.t1_img = pygame.transform.scale(token1_img,(self.cell_size-2,self.cell_size-2))
        token2_img=pygame.image.load("images/token2.png")
        self.t2_img = pygame.transform.scale(token2_img,(self.cell_size-2,self.cell_size-2))
        self.last_animate_time=0
        self.last_move=None
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
        return np.all(self.board != -1)
        
    def valid_check(self,j):
        return 0<=j<self.c and self.board[0][j]==-1
    
    def move(self,j):
        self.last_animate_time=pygame.time.get_ticks()/1000
        i=self.r-1
        while i>=0 and self.board[i][j]!=-1 :
            i=i-1
        self.board[i][j]=self.turn
        self.last_move=(i,j)

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

    def drawfallingball(self,r,c):
        color = "red" if self.board[r][c] == 0 else "yellow"
        t=pygame.time.get_ticks()/1000-self.last_animate_time
        cx = self.base_pos.x + c * self.cell_size + self.cell_size/2
        groundbasey = self.base_pos.y + r * self.cell_size + self.cell_size
        topbasey = self.base_pos.y
        t_bounce=2*np.sqrt(2*(groundbasey-topbasey)/fall_acc)
        t+=t_bounce/2
        vel=np.sqrt(2*fall_acc*(groundbasey-topbasey))
        t_sum_bounces=0
        count=0
        while t_bounce<t:
            t-=t_bounce
            if count>max_bounces:
                cy = groundbasey - self.cell_size/2
                pygame.draw.circle(self.screen,color,(cx, cy), 35)
                return
            vel*=coeff_restitution
            t_bounce*=coeff_restitution
            count+=1
        baseposfromgroundy=vel*t-0.5*fall_acc*t*t
        cy=groundbasey-baseposfromgroundy-self.cell_size/2
        pygame.draw.circle(self.screen,color,(cx, cy), 35)

    def drawboard(self):
        self.board_surface = pygame.Surface((self.cell_size*self.c,self.cell_size*self.r))
        self.board_surface.fill(grid_color)
        self.board_surface.set_colorkey(trans_color)
        for r in range(self.r):
            for c in range(self.c):
                cx = c * self.cell_size + self.cell_size/2
                cy = r * self.cell_size + self.cell_size/2
                pygame.draw.circle(self.board_surface, trans_color, (cx, cy), 35)
        for r in range(self.r):
            for c in range(self.c):
                cx = self.base_pos.x + c * self.cell_size + self.cell_size/2
                cy = self.base_pos.y + r * self.cell_size + self.cell_size/2
                if self.board[r][c] != -1 and (r,c)!=self.last_move:
                    color = "red" if self.board[r][c] == 0 else "yellow"
                    pygame.draw.circle(self.screen, color, (cx, cy), 35)
        if self.last_move is not None:
            self.drawfallingball(self.last_move[0],self.last_move[1])
        self.screen.blit(self.board_surface,self.base_pos)

        if self.win_animation_active:
            self.drawline()

    def specificmousepressevents(self,eventpos):
        j=int((eventpos[0]-self.base_pos.x)//self.cell_size)
        i=int((eventpos[1]-self.base_pos.y)//self.cell_size)
        if self.resultscreen or self.win_animation_active:
            return
        if self.valid_check(j):
            self.move(j)
            if self.win_check(self.last_move[0],self.last_move[1]):
                self.win_animation_active = True
                self.win_animation_start = pygame.time.get_ticks() / 1000.0
            elif self.draw_check():
                self.result = "DRW"
                self.resultscreen = True
            else:
                self.switch_turn()