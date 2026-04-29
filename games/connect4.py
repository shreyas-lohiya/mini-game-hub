import numpy as np
import pygame

from games.game_template import Game

b_height            = 8
b_width             = 8
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
    #sets the last time animation was called,last move, boolean indicating whether win animation is active along with caption
    def __init__(self,p1,p2,screen,theme):
        super().__init__(p1,p2,b_height,b_width,80,35,screen,theme)
        self.last_animate_time=0
        self.last_move=None
        self.win_animation_active=False
        pygame.display.set_caption("Connect4")

    #checks win or not along a specific direction also stores the value for animation if someone wins later
    #x_1 is x coordinates if we move along the given direction, index being given in the indices
    #similarly x_2 is in the opposite dirn, and y_1 y_2 are similarly defined for the y coordinate
    #masks are used to only restrict to the values that are valid in the cell
    #line_1,line_2 store 1,0 depending on whether the token is of the player from whom whichever we are checking the win
    #then k_1, k_2 are calculated which are the indices farthest away from the current cell (i,j) and till which all the cells have same token as self.turn
    #which is also number of cells from the current cells having same token as self.turn
    #then we simply compare k_1+1+k_2 with k to determine win
    def check_dirn(self,i,j,k,dirn):
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
        
    #checks win_check by iterating over all 4 directions
    def win_check(self,i,j,k=4):
        if self.check_dirn(i,j,k,[0,1]):
            return True
        elif self.check_dirn(i,j,k,[1,0]):
            return True
        elif self.check_dirn(i,j,k,[1,1]):
            return True
        elif self.check_dirn(i,j,k,[1,-1]):
            return True
        else:
            return False
    
    #draw if whole board is filled that is no cell is -1 anymore
    def draw_check(self):
        return np.all(self.board != -1)
      
    #checks if given j value is a valid column index for the next move  
    def valid_check(self,j):
        return 0<=j<self.c and self.board[0][j]==-1
    
    #finds which place to keep the next token and sets its new value along with updating last animation time
    def move(self,j):
        i=self.r-1
        while i>=0 and self.board[i][j]!=-1 :
            i=i-1
        self.board[i][j]=self.turn
        self.last_move=(i,j)
        self.last_animate_time=pygame.time.get_ticks()/1000

    #draws line if win animation is active, and sets the result once the animation is ended
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

    #calculates the distance of the token from the ground using Newton's law, coefficient restitution, uniform acceleration,
    #capped aafter few bounces, and
    #then draws token at calculated place so that it appears to fall
    def drawfallingtoken(self,r,c):
        color = "red" if self.board[r][c] == 0 else "yellow"
        t=pygame.time.get_ticks()/1000-self.last_animate_time
        cx = self.base_pos.x + c * self.cell_size + self.cell_size/2
        groundbasey = self.base_pos.y + r * self.cell_size + self.cell_size
        topbasey = self.base_pos.y
        t_bounce=2*np.sqrt(2*(groundbasey-topbasey)/fall_acc)
        t+=t_bounce/2
        vel=np.sqrt(2*fall_acc*(groundbasey-topbasey))
        count=0
        while t_bounce<t:
            t-=t_bounce
            if count>max_bounces:
                cy = groundbasey - self.cell_size/2
                pygame.draw.circle(self.screen,color,(cx, cy), self.piece_radius)
                return
            vel*=coeff_restitution
            t_bounce*=coeff_restitution
            count+=1
        baseposfromgroundy=vel*t-0.5*fall_acc*t*t
        cy=groundbasey-baseposfromgroundy-self.cell_size/2
        pygame.draw.circle(self.screen,color,(cx, cy), self.piece_radius)

    #draws the board along with the animating token falling and line in case someone wins
    def drawboard(self):
        self.board_surface = pygame.Surface((self.cell_size*self.c,self.cell_size*self.r))
        self.board_surface.fill(grid_color)
        self.board_surface.set_colorkey(trans_color)
        for r in range(self.r):
            for c in range(self.c):
                cx = c * self.cell_size + self.cell_size/2
                cy = r * self.cell_size + self.cell_size/2
                pygame.draw.circle(self.board_surface, trans_color, (cx, cy), self.piece_radius)
        for r in range(self.r):
            for c in range(self.c):
                cx = self.base_pos.x + c * self.cell_size + self.cell_size/2
                cy = self.base_pos.y + r * self.cell_size + self.cell_size/2
                if self.board[r][c] != -1 and (r,c)!=self.last_move:
                    color = "red" if self.board[r][c] == 0 else "yellow"
                    pygame.draw.circle(self.screen, color, (cx, cy), self.piece_radius)
        if self.last_move is not None:
            self.drawfallingtoken(self.last_move[0],self.last_move[1])
        self.screen.blit(self.board_surface,self.base_pos)

        if self.win_animation_active:
            self.drawline()

    #sees if win animation is active or not, if not then
    #calculates which cell is trying to get placed upon, sees validity,
    #then it moves and switches turn while checking win and draw
    def specificmousepressevents(self,eventpos):
        if self.win_animation_active:
            return
        j=int((eventpos[0]-self.base_pos.x)//self.cell_size)
        i=int((eventpos[1]-self.base_pos.y)//self.cell_size)
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