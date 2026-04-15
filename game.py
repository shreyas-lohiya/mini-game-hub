import sys
import os
import numpy as np
import pygame
import matplotlib.pyplot as plt
import csv

class Game:
    def __init__(self,p1,p2,r,c):
        self.p1=p1
        self.p2=p2
        self.turn=0
        self.board=np.full((r,c),-1)
        self.r=r
        self.c=c
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
    
class GameEngine:
    def __init__(self,p1,p2):
        self.p1=p1
        self.p2=p2

    def run(self):
        while True:
            choice=self.menu()
            game=self.load(choice)
            winner=game.play()
            if winner=="DRW":
                print ("The Game is Draw")
            else :
                print ("The winner is "+winner)

            if not self.play_again():
                break
                
    def menu(self):
        pygame.init()
        res=(1280,720)
        bg_color=(18,18,18)
        button_color=(40,40,40)
        hover_color=(70,130,180)
        text_color=(235,235,235)
        screen=pygame.display.set_mode(res)
        pygame.display.set_caption("Mini Game Hub")
        font = pygame.font.SysFont("segoeui", 36)
        buttons = {
        "Tic-Tac-Toe": pygame.Rect(510,230,250,60),
        "Othello": pygame.Rect(510,325,250,60),
        "Connect4": pygame.Rect(510,420,250,60)
        }
        texts = {}
        for name, rect in buttons.items():
            texts[name] = font.render(name.upper(),True,text_color)
        clock= pygame.time.Clock()

        while True:
            screen.fill(bg_color)
            mouse_pos=pygame.mouse.get_pos()

            for name, rect in buttons.items():
                if rect.collidepoint(mouse_pos):
                    color=hover_color
                else:
                    color=button_color
                pygame.draw.rect(screen, color, rect, border_radius=10)
                text = texts[name]
                text_rect=text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for name, rect in buttons.items():
                        if rect.collidepoint(mouse_pos):
                            return name
            clock.tick(30)
    
    def load(self,c):
        if c == "Tic-Tac-Toe":
            from games.tictactoe import TicTacToe
            return TicTacToe(self.p1,self.p2)
        elif c == "Othello":
            from games.othello import Othello
            return Othello(self.p1,self.p2)
        elif c == "Connect4":
            from games.connect4 import Connect4
            return Connect4(self.p1,self.p2)
    
    def play_again(self):
        pass

def plotstuff():
    totwins={}
    gameplayfreq={'tictactoe':0, 'othello':0, 'connect4':0}
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
    plt.show()

def main():
    player1=sys.argv[1]
    player2=sys.argv[2]
    engine=GameEngine(player1, player2)
    engine.run()

if __name__ == "__main__":
    main()
