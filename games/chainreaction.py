# import numpy as np
# import pygame

# from game import Game,Button


# b_height=6
# b_width=9
# fps=60
# grid=100

# class ChainRxn(Game):

#     def __init__(self,p1,p2,screen,theme):
#         super().__init__(p1,p2,b_height,b_width,screen,theme)
#         self.board=np.zeros((b_height,b_width))

#     def we_ball(self,i,j,k):
#         cx=190+(j)*grid+grid/2
#         cy=60+(i)*grid+grid/2
#         if self.board[i][j]>0:
#             if(self.theme=="Phonk"):
#                 color="yellow"
#             else:
#                 color="green"
#         else:
#             if (self.theme=="Phonk"):
#                 color="green"
#             else:
#                 color="green"
#         if(k==1):
#             pygame.draw.circle(self.screen,color,(cx,cy),20)
#         if(k==2):
#             pygame.draw.circle(self.screen,color,(cx-21,cy),20)
#             pygame.draw.circle(self.screen,color,(cx+21,cy),20)
#         if(k==3):
#             pygame.draw.circle(self.screen,color,(cx,cy-19),20)
#             pygame.draw.circle(self.screen,color,(cx-21,cy+15),20)
#             pygame.draw.circle(self.screen,color,(cx+21,cy+15),20)

#     def pop(self,i,j):
#         if (i==0 or i==self.r-1) and (j==0 or j==self.c-1):
#             return 2
#         elif i==0 or i==self.r-1 or j==0 or j==self.c-1:
#             return 3
#         else:
#             return 4 
    
#     def win_check(self):
#         b=self.board
#         if (np.sum(b[b>0]) == np.sum(b)) and (np.sum(b)!=0) and np.sum(b>0)>1:
#             return True
#         elif np.sum(b[b<0]) == np.sum(b) and (np.sum(b)!=0) and np.sum(b<0)>1:
#             return True
#         else:
#             return False
    
#     def valid_check(self,i,j):
#         if self.board[i][j]==0:
#             return True
#         elif (self.board[i][j]>0 and self.turn==0):
#             return True
#         elif (self.board[i][j]<0 and self.turn==1):
#             return True
#         else:
#             return False
    
#     def move(self,i,j):

#         if self.turn==0:
#             self.board[i][j]+=1
#         if self.turn==1:
#             self.board[i][j]-=1

#         capacity = self.pop(i, j)

#         if abs(self.board[i][j])>=capacity:
#             self.board[i][j] = 0
#             if i>0:
#                 self.board[i-1][j]=abs(self.board[i-1][j]) * (1 if self.turn == 0 else -1)
#                 self.move(i-1,j)
#             if i<self.r-1:
#                 self.board[i+1][j]=abs(self.board[i+1][j]) * (1 if self.turn == 0 else -1)
#                 self.move(i+1,j)
#             if j>0:
#                 self.board[i][j-1]=abs(self.board[i][j-1]) * (1 if self.turn == 0 else -1)
#                 self.move(i,j-1)
#             if j<self.c-1:
#                 self.board[i][j+1]=abs(self.board[i][j+1]) * (1 if self.turn == 0 else -1)
#                 self.move(i,j+1)

#     def play(self):
#         bg_color = (0,0,18)
#         line_color = (200,200,200)
#         quitscreen=False
#         resultscreen=False
#         drawclaimed=False
#         pygame.display.set_caption("Chain-Reaction")

#         cells = []
#         cell_w = grid
#         cell_h = grid

#         for x in range(self.r):
#             for y in range(self.c):
#                 left=190+y*cell_w
#                 top=60+x*cell_h
#                 rect=pygame.Rect(left,top,cell_w,cell_h)
#                 cells.append(rect)
        
#         while True:
#             dt = self.clock.tick(fps)/1000
#             self.screen.fill(bg_color)
#             self.screen.blit(self.bg,(0,0))
#             for rect in cells:
#                 pygame.draw.rect(self.screen,line_color,rect,1) 
#             mouse_pos = pygame.mouse.get_pos()
#             for i in range(self.r):
#                 for j in range(self.c):
#                     if np.abs(self.board[i][j])>=1 and np.abs(self.board[i][j])<=3:
#                         rect = cells[i*self.c + j]
#                         self.we_ball(i,j,np.abs(self.board[i][j]))
                        
#             player1=self.font.render(f"{self.p1}", True, (200, 200, 200))
#             self.screen.blit(player1, player1.get_rect(center=(self.screen.get_width()/2-400,120)))
#             player2=self.font.render(f"{self.p2}", True, (200, 200, 200))
#             self.screen.blit(player2, player2.get_rect(center=(self.screen.get_width()/2+400,120)))
#             self.btnresign1.draw(pygame.mouse.get_pos(),dt,self.screen)
#             self.btnresign2.draw(pygame.mouse.get_pos(),dt,self.screen)
#             self.btnclaimdraw1.draw(pygame.mouse.get_pos(),dt,self.screen)
#             self.btnclaimdraw2.draw(pygame.mouse.get_pos(),dt,self.screen)
#             if quitscreen :
#                 title=self.font.render("You sure you wanna quit ?", True, (200, 200, 200))
#                 title = pygame.transform.scale_by(title,1+0.05*np.sin(pygame.time.get_ticks()/200))
#                 self.screen.blit(title, title.get_rect(center=(self.screen.get_width()/2,120)))
#                 self.btnquityes.draw(pygame.mouse.get_pos(),dt,self.screen)
#                 self.btnquitno.draw(pygame.mouse.get_pos(),dt,self.screen)
#             elif resultscreen :
#                 if result=="DRW":
#                     title=self.font.render("DRAW", True, (200, 200, 200))
#                     title = pygame.transform.scale_by(title,1+0.05*np.sin(pygame.time.get_ticks()/200))
#                     self.screen.blit(title, title.get_rect(center=(self.screen.get_width()/2,self.screen.get_height()/2)))
#                 else:
#                     title=self.font.render(f"WINNER IS {result}", True, (200, 200, 200))
#                     title = pygame.transform.scale_by(title,1+0.05*np.sin(pygame.time.get_ticks()/200))
#                     self.screen.blit(title, title.get_rect(center=(self.screen.get_width()/2,self.screen.get_height()/2)))
#                 self.btnproceedresult.draw(pygame.mouse.get_pos(),dt,self.screen)
#             elif drawclaimed:
#                 title=self.font.render(f"{whoclaimdraw} claimed draw", True, (200, 200, 200))
#                 title = pygame.transform.scale_by(title,1+0.05*np.sin(pygame.time.get_ticks()/200))
#                 self.screen.blit(title, title.get_rect(center=(self.screen.get_width()/2,self.screen.get_height()/2)))
#                 self.btnacceptdraw.draw(pygame.mouse.get_pos(),dt,self.screen)
#                 self.btnrejectdraw.draw(pygame.mouse.get_pos(),dt,self.screen)
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     quitscreen=True
#                 if event.type == pygame.MOUSEBUTTONDOWN:
#                     if quitscreen:
#                         if self.btnquityes.pressed(pygame.mouse.get_pos()):
#                             return None
#                         elif self.btnquitno.pressed(pygame.mouse.get_pos()):
#                             quitscreen=False
#                     elif resultscreen:
#                         if self.btnproceedresult.pressed(pygame.mouse.get_pos()):
#                             return result
#                     elif drawclaimed:
#                         if self.btnacceptdraw.pressed(pygame.mouse.get_pos()):
#                             result = "DRW"
#                             resultscreen=True
#                         elif self.btnrejectdraw.pressed(pygame.mouse.get_pos()):
#                             drawclaimed=False
#                     elif self.btnresign1.pressed(pygame.mouse.get_pos()):
#                         result = self.p2
#                         resultscreen = True
#                     elif self.btnresign2.pressed(pygame.mouse.get_pos()):
#                         result = self.p1
#                         resultscreen = True
#                     elif self.btnclaimdraw1.pressed(pygame.mouse.get_pos()):
#                         whoclaimdraw = self.p1
#                         drawclaimed = True
#                     elif self.btnclaimdraw2.pressed(pygame.mouse.get_pos()):
#                         whoclaimdraw = self.p2
#                         drawclaimed = True
#                     else:
#                         for rect in cells:
#                             if rect.collidepoint(mouse_pos):
#                                 i = int((rect.top - 60)//cell_h)
#                                 j = int((rect.left - 190)//cell_w)
#                                 if self.valid_check(i,j):
#                                     self.move(i,j)
#                                     if self.win_check():
#                                         if self.turn==0:
#                                             result = self.p1
#                                             resultscreen = True
#                                         else:
#                                             result = self.p2
#                                             resultscreen = True
#                                     self.switch_turn()
#             pygame.display.flip()

import numpy as np
import pygame
from game import Game

b_height=9
b_width=6
fps=60
bg_color = (0,0,18)
line_color = (200,200,200)
grid_width = 1 
animate_time = 0.2

class ChainRxn(Game):

    def __init__(self,p1,p2,screen,theme):
        self.cell_size_original = 70
        super().__init__(p1,p2,b_height,b_width,screen,theme)
        self.board=np.zeros((b_height,b_width))
        pygame.display.set_caption("CHAIN REACTION")
        self.capacity=np.zeros((b_height,b_width))
        for i in range(self.r):
            for j in range(self.c):
                if (i==0 or i==self.r-1) and (j==0 or j==self.c-1):
                    self.capacity[i][j]=2
                elif i==0 or i==self.r-1 or j==0 or j==self.c-1:
                    self.capacity[i][j]=3
                else:
                    self.capacity[i][j]=4 
        self.canmove=True
        self.last_update_time=0
        self.needtoexplode=[]
    
    def win_check(self):
        b=self.board
        if np.all(b>=0) and np.sum(b>0)>1:
            return True
        elif np.all(b<=0) and np.sum(b<0)>1:
            return True
        else:
            return False
    
    def valid_check(self,i,j):
        if i<0 or j<0 or i >= self.r or j >=self.c:
            return False
        elif self.board[i][j]==0:
            return True
        elif (self.board[i][j]>0 and self.turn==0):
            return True
        elif (self.board[i][j]<0 and self.turn==1):
            return True
        else:
            return False
    
    def move(self,i,j):
        self.board[i][j] += 1 - 2*self.turn
        self.last_update_time=pygame.time.get_ticks()/1000
            
    def updateboard(self):
        self.last_update_time=pygame.time.get_ticks()/1000
        self.oldboard=self.board.copy()
        for i in range(self.r):
            for j in range(self.c):
                if abs(self.oldboard[i][j])>=self.capacity[i][j]:
                    if i>0:
                        self.board[i-1][j]=(abs(self.board[i-1][j])+1)*np.sign(self.oldboard[i][j])
                    if i<self.r-1:
                        self.board[i+1][j]=(abs(self.board[i+1][j])+1)*np.sign(self.oldboard[i][j])
                    if j>0:
                        self.board[i][j-1]=(abs(self.board[i][j-1])+1)*np.sign(self.oldboard[i][j])
                    if j<self.c-1:
                        self.board[i][j+1]=(abs(self.board[i][j+1])+1)*np.sign(self.oldboard[i][j])
                    self.board[i][j]-=np.sign(self.board[i][j])*self.capacity[i][j]
        if self.win_check():
                if self.turn==0:
                    self.result = self.p1
                else:
                    self.result = self.p2
                self.resultscreen = True
                    
                    
    def drawboard(self):
        ball_radius=14*min(self.screen.get_width()/1280, self.screen.get_height()/720)
        t=pygame.time.get_ticks()/1000-self.last_update_time
        if t>animate_time and np.any(abs(self.board)>=self.capacity):
            self.updateboard()
        t=pygame.time.get_ticks()/1000-self.last_update_time
        for i in range(self.r):
            for j in range(self.c):
                pygame.draw.rect(self.screen,line_color,(self.base_pos.x+j*self.cell_size,self.base_pos.y+i*self.cell_size,self.cell_size,self.cell_size),width=grid_width)
                cx=self.base_pos.x+(j)*self.cell_size+self.cell_size/2
                cy=self.base_pos.y+(i)*self.cell_size+self.cell_size/2
                color = "red" if self.board[i][j]>0 else "green"
                value = abs(self.board[i][j])
                if value>=self.capacity[i][j]:
                    value-=self.capacity[i][j]
                    distance=(self.cell_size-ball_radius/2)*(t/animate_time)
                    if i>0:
                        pygame.draw.circle(self.screen,color,(cx,cy-distance),ball_radius)
                    if i<self.r-1:
                        pygame.draw.circle(self.screen,color,(cx,cy+distance),ball_radius)
                    if j>0:
                        pygame.draw.circle(self.screen,color,(cx-distance,cy),ball_radius)
                    if j<self.c-1:
                        pygame.draw.circle(self.screen,color,(cx+distance,cy),ball_radius)
                if value>=1:
                    if(value==1):
                        pygame.draw.circle(self.screen,color,(cx,cy),ball_radius)
                    elif(value==2):
                        pygame.draw.circle(self.screen,color,(cx-ball_radius,cy),ball_radius)
                        pygame.draw.circle(self.screen,color,(cx+ball_radius,cy),ball_radius)
                    elif(value==3):
                        pygame.draw.circle(self.screen,color,(cx,cy-ball_radius),ball_radius)
                        pygame.draw.circle(self.screen,color,(cx-ball_radius,cy+0.75*ball_radius),ball_radius)
                        pygame.draw.circle(self.screen,color,(cx+ball_radius,cy+0.75*ball_radius),ball_radius)

                    
    def specificmousepressevents(self, eventpos):
        j=int((eventpos[0]-self.base_pos.x)//self.cell_size)
        i=int((eventpos[1]-self.base_pos.y)//self.cell_size)
        if self.valid_check(i,j) and np.all(abs(self.board)<self.capacity):
            self.move(i,j)
            self.switch_turn()
    


    
