import sys
import numpy as np
import pygame
import matplotlib.pyplot as plt
import csv
from datetime import date
import subprocess

res                 = (1280,720)
bg_color            = (18,18,18)
button_color        = (40,40,40)
hover_color         = (70,130,180)
text_color          = (235,235,235)
fps                 = 60

class Game:
    def __init__(self,p1,p2,r,c,screen):
        self.p1=p1
        self.p2=p2
        self.turn=0
        self.board=np.full((r,c),-1)
        self.r=r
        self.c=c
        self.screen=screen
    def switch_turn(self):
        self.turn=1-self.turn
    def win_check(self,i,j):
        raise NotImplementedError
    def draw_check(self):
        raise NotImplementedError
    def valid_check(self,i,j):
        raise NotImplementedError
    def move(self,i,j):
        raise NotImplementedError
    def play(self):
        raise NotImplementedError
    
class GameEngine:
    def __init__(self,p1,p2,screen):
        self.p1=p1
        self.p2=p2
        self.screen=screen
        self.title_font=pygame.font.SysFont("segoeui", 64, bold=True)
        self.button_font=pygame.font.SysFont("segoeui", 36)
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            pygame.display.set_caption("Mini Game Hub")
            choice=self.menu("CHOOSE A GAME","Tic-Tac-Toe", "Othello", "Connect4", "Chain-Reaction")
            if choice is None:
                return
            game=self.load(choice)
            winner=game.play()
            pygame.display.set_caption("Mini Game Hub")
            today = date.today()
            with open('history.csv', 'a') as f:
                if winner is None:
                    return
                if winner=="DRW":
                    f.write(f"{self.p1},{self.p2},{today},{choice},True\n")
                elif winner==self.p1:
                    f.write(f"{self.p1},{self.p2},{today},{choice},False\n")
                else:
                    f.write(f"{self.p2},{self.p1},{today},{choice},False\n")
            metric=self.menu("METRIC FOR LEADERBOARD","User","Wins","Draws","Losses","Wins/Losses")
            siz=pygame.display.get_window_size()
            #pos=pygame.display.get_window_position()
            #pygame.display.set_window_position ((0,0))
            pygame.display.set_mode((1,1))
            subprocess.run(["./leaderboard.sh", metric])
            pygame.display.set_mode(siz)
            #pygame.display.set_window_position (pos)
            self.plotstuff()
            choice=self.menu("WANNA PLAY AGAIN?","Play again","Quit")
            if choice is None or choice=="Quit":
                break
    
    class Button:
        def __init__(self, text, center,button_font):
            self.text = text
            self.base_rect = pygame.Rect(0, 0, 320, 70)
            self.base_rect.center = center
            self.button_font=button_font
            self.t = 0
            self.rect= self.base_rect.copy()
        def draw(self, mouse_pos, dt, screen):
            scale = 1 + 0.1 * self.t
            w = self.base_rect.width * scale
            h = self.base_rect.height * scale
            self.rect = pygame.Rect(0, 0, w, h)
            self.rect.center = self.base_rect.center
            if self.rect.collidepoint(mouse_pos):
                self.t = min(1, self.t + (1-self.t)*10*dt)
            else:
                self.t = max(0, self.t - self.t*10*dt)
            self.rect.centery-=5*self.t
            color = (
                int(button_color[0] + (hover_color[0] - button_color[0]) * self.t),
                int(button_color[1] + (hover_color[1] - button_color[1]) * self.t),
                int(button_color[2] + (hover_color[2] - button_color[2]) * self.t)
            )
            pygame.draw.rect(screen, color, self.rect, border_radius=14)
            txt = self.button_font.render(self.text.upper(), True, text_color)
            txt_rect = txt.get_rect(center=self.rect.center)
            screen.blit(txt, txt_rect)
            return self.rect
        
        def pressed(self, mouse_pos):
            return self.rect.collidepoint(mouse_pos)

    def menu(self,heading,*names):
        buttons = []
        for i, name in enumerate(names):
            buttons.append(self.Button(name,(self.screen.get_width()/2,self.screen.get_height()/2-120+i*100),self.button_font))
        while True:
            dt=self.clock.tick(fps)/1000
            mouse_pos=pygame.mouse.get_pos()
            self.screen.fill(bg_color)
            title = self.title_font.render(heading, True, (200, 200, 200))
            title = pygame.transform.scale_by(title,1+0.05*np.sin(pygame.time.get_ticks()/200))
            self.screen.blit(title, title.get_rect(center=(self.screen.get_width()/2, 120)))
            for btn in buttons:
                btn.draw(mouse_pos,dt,self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for btn in buttons:
                        if btn.pressed(mouse_pos):
                            return btn.text
            pygame.display.flip()

    def load(self,c):
        if c == "Tic-Tac-Toe":
            from games.tictactoe import TicTacToe
            return TicTacToe(self.p1,self.p2,self.screen)
        elif c == "Othello":
            from games.othello import Othello
            return Othello(self.p1,self.p2,self.screen)
        elif c == "Connect4":
            from games.connect4 import Connect4
            return Connect4(self.p1,self.p2,self.screen)
        elif c == "Chain-Reaction":
            from games.chainreaction import ChainRxn
            return ChainRxn(self.p1,self.p2,self.screen)
    
    def play_again(self):
        pass

    def plotstuff(self):
        totwins={}
        gameplayfreq = {
        'Tic-Tac-Toe': 0,
        'Othello': 0,
        'Connect4': 0,
        'Chain-Reaction': 0
        }
        with open('history.csv') as f:
            for field in csv.reader(f):
                if field[0] in totwins:
                    totwins[field[0]]+=1
                else:
                    totwins[field[0]]=1
                if field[1] not in totwins:
                    totwins[field[1]]=0
                gameplayfreq[field[3]]+=1
        sortedtotwins = sorted(totwins.items(), key=lambda x: x[1], reverse=True)
        top5=[]
        for item in sortedtotwins:
            if len(top5)<5:
                top5.append(item)
            elif item[1]==top5[4][1]:
                top5.append(item)
            else:
                break
        fontforplottitle = {'family':'serif','color':'blue','size':20}
        plt.subplot(2,2,1)
        plt.bar([x[0] for x in top5],[x[1] for x in top5])
        plt.title("Top 5 Players",fontdict=fontforplottitle)
        plt.ylabel("Total number of wins")
        plt.subplot(2,2,2)
        plt.pie(list(totwins.values()),labels=list(totwins.keys()))
        plt.title("Total number of wins",fontdict=fontforplottitle)
        plt.subplot(2,1,2)
        plt.pie(list(gameplayfreq.values()),labels=list(gameplayfreq.keys()))
        plt.title("Most Played Games",fontdict=fontforplottitle)
        plt.tight_layout()
        plt.savefig("plot.png")
        plt.close('all')
        plotimg = pygame.image.load("plot.png")
        subprocess.run(["rm", "plot.png"])
        btn = self.Button("PROCEED",(self.screen.get_width()/2,self.screen.get_height()-50),self.button_font)
        while True:
            dt=self.clock.tick(fps)/1000
            mouse_pos=pygame.mouse.get_pos()
            self.screen.fill((255,255,255))
            rect=plotimg.get_rect(center=(self.screen.get_width()/2,self.screen.get_height()/2))
            self.screen.blit(plotimg, rect)
            btn.draw(mouse_pos,dt,self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if btn.pressed(mouse_pos):
                        return
            pygame.display.flip()

def main():
    pygame.init()
    player1=sys.argv[1]
    player2=sys.argv[2]
    screen=pygame.display.set_mode(res)
    engine=GameEngine(player1, player2,screen)
    engine.run()
    pygame.quit()

if __name__ == "__main__":
    main()