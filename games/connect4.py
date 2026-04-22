import sys
import os
import numpy
import pygame

from game import Game

res = (1280,720)
bg_color = (0,0,18)
line_color = (200,200,200)
fps=60
fall_time=1

class Connect4(Game):

    def __init__(self,p1,p2,screen):
        self.p1=p1
        self.p2=p2
        super().__init__(p1,p2,7,7,screen)
    
    def anim_yellow_token(self, x, y):
        fx = x + 40
        sy = 40
        fy = y + 40

        pos_y = sy
        speed = 800

        while True:
            dt = self.clock.tick(60) /1000
            pos_y += speed * dt
            if(pos_y>=fy):
                pos_y = fy
            self.screen.fill(bg_color)
            pygame.draw.circle(self.screen,"yellow",(fx,int(pos_y)),35)

            self.screen.blit(self.board_surface, (360,80))

            pygame.display.update()

            if pos_y==fy:
                break
        self.running=True
    
    def yellow_token(self,x,y):
        cx=x+40 
        cy=y+40
        pygame.draw.circle(self.screen,"yellow",(cx, cy),35)
    
    def red_token(self,x,y):
        cx=x+40 
        cy=y+40
        pygame.draw.circle(self.screen,"red",(cx, cy),35)
    
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
        pygame.display.set_caption("Connect4")

        cells = []
        cell_w = int(560/self.c)
        cell_h = int(560/self.r)
        self.clock = pygame.time.Clock()

        for x in range(self.r):
            for y in range(self.c):
                left=360+y*cell_w
                top=80+x*cell_h
                rect=pygame.Rect(left,top,cell_w,cell_h)
                cells.append(rect)
        self.board_surface = pygame.Surface([560,560],pygame.SRCALPHA)
        self.board_surface.fill((0, 0, 255, 255))
        for row in range(self.r):
            for col in range(self.c):
                x = col * cell_w + cell_w/2
                y = row * cell_h + cell_h/2
                pygame.draw.circle(self.board_surface,(0, 0, 0, 0),(x, y),35)

        self.running=True
        while self.running:
            self.screen.fill(bg_color)
            self.screen.blit(self.board_surface, (360,80)) 
            mouse_pos = pygame.mouse.get_pos()
            for i in range(self.r):
                for j in range(self.c):
                    if self.board[i][j] == 0:
                        rect = cells[i*self.c+j]
                        self.red_token(rect.left+1,rect.top+1)
                    if self.board[i][j] == 1:
                        rect = cells[i*self.c + j]
                        self.yellow_token(rect.left+1,rect.top+1)
                    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x = event.pos[0]
                    j = int((x - 360) // cell_w)
                    if 0 <= j < self.c and self.valid_check(j):
                        i = self.move(j)
                        rect = cells[i*self.c + j]

                        if self.turn == 0:
                            colour = "red"
                        else:
                            colour = "yellow"

                        fx = rect.left + 40
                        fy = rect.top + 40
                        sy = 80
                        pos_y = sy
                        speed = 400

                        self.board[i][j] = -1

                        while True:
                            dt = self.clock.tick(60) / 1000

                            if pos_y >= fy:
                                pos_y = fy

                            for event2 in pygame.event.get():
                                if event2.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()

                            self.screen.fill(bg_color)

                            for r in range(self.r):
                                for c in range(self.c):
                                    if self.board[r][c] == 0:
                                        rrect = cells[r*self.c + c]
                                        self.red_token(rrect.left+1, rrect.top+1)
                                    elif self.board[r][c] == 1:
                                        rrect = cells[r*self.c + c]
                                        self.yellow_token(rrect.left+1, rrect.top+1)

                            pygame.draw.circle(self.screen, colour, (fx, int(pos_y)), 35)
                            self.screen.blit(self.board_surface, (360, 80))
                            pygame.display.update()

                            if pos_y == fy:
                                break
                            pos_y += speed * dt

                        self.board[i][j] = self.turn

                        if self.win_check(i, j):
                            return self.p1 if self.turn == 0 else self.p2

                        self.switch_turn()

                        if self.draw_check():
                            return "DRW"
    
            pygame.display.flip()