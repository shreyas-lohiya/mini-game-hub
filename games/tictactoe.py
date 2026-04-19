import numpy as np
import pygame

from game import Game,Button

fps=60 

class TicTacToe(Game):

    def __init__(self,p1,p2,screen,theme):
        super().__init__(p1,p2,10,10,screen,theme)

    def dirn(self,i,j,k,dirn):
        indice = np.arange(-k+1,k)
        x = i+dirn[0]*indice
        y = j+dirn[1]*indice
        mask = (x>=0)&(x<self.r)&(y>=0)&(y<self.c)
        line = self.board[x[mask], y[mask]]
        fin = np.where(line==self.turn,1,0)
        if np.any(np.convolve(fin,np.ones(k),'valid')==k):
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
        if (self.board == -1).sum() == 0:
            return True
        else:
            return False
        
    def valid_check(self,i,j):
        return self.board[i][j]==-1
    
    def move(self,i,j):
        self.board[i][j]=self.turn
            
    def play(self):
        res = (1280,720)
        bg_color = (0,0,18)
        line_color = (200,200,200)
        quitscreen=False
        resultscreen=False
        drawclaimed=False
        pygame.display.set_caption("Tic-Tac-Toe")

        cells = []
        cell_w = int(600/self.c)
        cell_h = int(600/self.r)

        for x in range(self.r):
            for y in range(self.c):
                left=340+y*cell_w
                top=60+x*cell_h
                rect=pygame.Rect(left,top,cell_w,cell_h)
                cells.append(rect)
        
        x_img=pygame.image.load("images/x.png")
        x_resized_img = pygame.transform.scale(x_img,(cell_w-2,cell_h-2))
        o_img=pygame.image.load("images/o.png")
        o_resized_img = pygame.transform.scale(o_img,(cell_w-2,cell_h-2))
        x_img.set_colorkey((0,0,18))
        o_img.set_colorkey((0,0,18))
        
    
        while True:
            dt = self.clock.tick(fps)/1000
            self.screen.fill(bg_color)
            self.screen.blit(self.bg,(0,0))
            for rect in cells:
                pygame.draw.rect(self.screen,line_color,rect,1) 
            mouse_pos = pygame.mouse.get_pos()
            for i in range(self.r):
                for j in range(self.c):
                    if self.board[i][j] == 0:
                        rect = cells[i*self.c+j]
                        self.screen.blit(x_resized_img,(rect.left+1,rect.top+1))
                    if self.board[i][j] == 1:
                        rect = cells[i*self.c + j]
                        self.screen.blit(o_resized_img,(rect.left+1,rect.top+1))
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
                        for rect in cells:
                            if rect.collidepoint(mouse_pos):
                                i = int((rect.top - 60)//cell_h)
                                j = int((rect.left - 340)//cell_w)
                                if self.valid_check(i,j) :
                                    self.move(i,j)
                                    if self.win_check(i,j):
                                        if self.turn==0:
                                            result = self.p1
                                            resultscreen = True
                                        else:
                                            result = self.p2
                                            resultscreen = True
                                    self.switch_turn()
                                    if self.draw_check():
                                        result = "DRW"
                                        resultscreen = True
            pygame.display.flip()

        
