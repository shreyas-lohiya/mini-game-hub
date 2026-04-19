import numpy as np
import pygame

from game import Game,Button

fps=60

class ChainRxn(Game):

    def __init__(self,p1,p2,screen,theme):
        super().__init__(p1,p2,6,9,screen,theme)
        self.board=np.zeros((6,9))

    def pop(self,i,j):
        if (i==0 or i==self.r-1) and (j==0 or j==self.c-1):
            return 2
        elif i==0 or i==self.r-1 or j==0 or j==self.c-1:
            return 3
        else:
            return 4 
    
    def own(self,i,j):
        if(self.board[i][j]==0):
            return -1
        elif(self.board[i][j]/abs(self.board[i][j])==1):
            return 0
        else:
            return 1
        
    
    def win_check(self):
        b=self.board
        if (np.sum(b[b>0]) == np.sum(b)) and (np.sum(b)!=0) and np.sum(b>0)>1:
            return True
        elif np.sum(b[b<0]) == np.sum(b) and (np.sum(b)!=0) and np.sum(b<0)>1:
            return True
        else:
            return False
    
    def valid_check(self,i,j):
        if self.board[i][j]==0:
            return True
        elif (self.board[i][j]>0 and self.turn==0):
            return True
        elif (self.board[i][j]<0 and self.turn==1):
            return True
        else:
            return False
    
    def move(self,i,j):

        if self.turn==0:
            self.board[i][j]+=1
        if self.turn==1:
            self.board[i][j]-=1

        capacity = self.pop(i, j)

        if abs(self.board[i][j])>=capacity:
            self.board[i][j] = 0
            if i>0:
                self.board[i-1][j]=abs(self.board[i-1][j]) * (1 if self.turn == 0 else -1)
                self.move(i-1,j)
            if i<self.r-1:
                self.board[i+1][j]=abs(self.board[i+1][j]) * (1 if self.turn == 0 else -1)
                self.move(i+1,j)
            if j>0:
                self.board[i][j-1]=abs(self.board[i][j-1]) * (1 if self.turn == 0 else -1)
                self.move(i,j-1)
            if j<self.c-1:
                self.board[i][j+1]=abs(self.board[i][j+1]) * (1 if self.turn == 0 else -1)
                self.move(i,j+1)

    def play(self):
        res = (1280,720)
        bg_color = (0,0,18)
        line_color = (200,200,200)
        quitscreen=False
        resultscreen=False
        drawclaimed=False
        pygame.display.set_caption("Chain-Reaction")

        cells = []
        cell_w = int(900/self.c)
        cell_h = int(600/self.r)

        for x in range(self.r):
            for y in range(self.c):
                left=190+y*cell_w
                top=60+x*cell_h
                rect=pygame.Rect(left,top,cell_w,cell_h)
                cells.append(rect)
        
        red1_img=pygame.image.load("images/red1.png")
        red1_resized_img = pygame.transform.scale(red1_img,(cell_w-2,cell_h-2))
        red2_img=pygame.image.load("images/red2.png")
        red2_resized_img = pygame.transform.scale(red2_img,(cell_w-2,cell_h-2))
        red3_img=pygame.image.load("images/red3.png")
        red3_resized_img = pygame.transform.scale(red3_img,(cell_w-2,cell_h-2))
        green1_img=pygame.image.load("images/green1.png")
        green1_resized_img = pygame.transform.scale(green1_img,(cell_w-2,cell_h-2))
        green2_img=pygame.image.load("images/green2.png")
        green2_resized_img = pygame.transform.scale(green2_img,(cell_w-2,cell_h-2))
        green3_img=pygame.image.load("images/green3.png")
        green3_resized_img = pygame.transform.scale(green3_img,(cell_w-2,cell_h-2))
        
        while True:
            dt = self.clock.tick(fps)/1000
            self.screen.fill(bg_color)
            self.screen.blit(self.bg,(0,0))
            for rect in cells:
                pygame.draw.rect(self.screen,line_color,rect,1) 
            mouse_pos = pygame.mouse.get_pos()
            for i in range(self.r):
                for j in range(self.c):
                    if self.board[i][j] == 1:
                        rect = cells[i*self.c + j]
                        self.screen.blit(red1_resized_img,(rect.left+1,rect.top+1))
                    if self.board[i][j] == 2:
                        rect = cells[i*self.c + j]
                        self.screen.blit(red2_resized_img,(rect.left+1,rect.top+1))
                    if self.board[i][j] == 3:
                        rect = cells[i*self.c + j]
                        self.screen.blit(red3_resized_img,(rect.left+1,rect.top+1))
                    if self.board[i][j] == -1:
                        rect = cells[i*self.c + j]
                        self.screen.blit(green1_resized_img,(rect.left+1,rect.top+1))
                    if self.board[i][j] == -2:
                        rect = cells[i*self.c + j]
                        self.screen.blit(green2_resized_img,(rect.left+1,rect.top+1))
                    if self.board[i][j] == -3:
                        rect = cells[i*self.c + j]
                        self.screen.blit(green3_resized_img,(rect.left+1,rect.top+1))
                        
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
                                j = int((rect.left - 190)//cell_w)
                                if self.valid_check(i,j):
                                    self.move(i,j)
                                    if self.win_check():
                                        if self.turn==0:
                                            result = self.p1
                                            resultscreen = True
                                        else:
                                            result = self.p2
                                            resultscreen = True
                                    self.switch_turn()
            pygame.display.flip()

    


    
