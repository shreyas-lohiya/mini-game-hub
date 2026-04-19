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
    def __init__(self,p1,p2,r,c,screen,theme):
        self.p1=p1
        self.p2=p2
        self.turn=0
        self.board=np.full((r,c),-1)
        self.r=r
        self.c=c
        self.screen=screen
        self.theme=theme
        pygame.mixer.music.load(f"music/{self.theme}.ogg")
        pygame.mixer.music.play(-1)
        self.bg = pygame.image.load(f"images/{self.theme}.png")
        self.bg = pygame.transform.scale(self.bg, self.screen.get_size())
        self.font = pygame.font.SysFont("segoeui", 36)
        self.btnquityes = Button("Yes",(self.screen.get_width()/2-100,self.screen.get_height()/2+100),self.font, 80, 40)
        self.btnquitno = Button("No",(self.screen.get_width()/2+100,  self.screen.get_height()/2+100),self.font, 80, 40)
        self.btnproceedresult = Button("Proceed",(self.screen.get_width()/2,  self.screen.get_height()/2+100),self.font, 320, 200)
        self.btnresign1 = Button("Resign",(self.screen.get_width()/2-400,self.screen.get_height()/2+100),self.font, 80, 40)
        self.btnresign2 = Button("Resign",(self.screen.get_width()/2+400,self.screen.get_height()/2+100),self.font, 80, 40)
        self.btnclaimdraw1 = Button("Claim Draw",(self.screen.get_width()/2-400,self.screen.get_height()/2+200),self.font, 80, 40)
        self.btnclaimdraw2 = Button("Claim Draw",(self.screen.get_width()/2+400,self.screen.get_height()/2+200),self.font, 80, 40)
        self.btnacceptdraw = Button("Accept",(self.screen.get_width()/2-100,self.screen.get_height()/2+100),self.font, 80, 40)
        self.btnrejectdraw = Button("Reject",(self.screen.get_width()/2+100,self.screen.get_height()/2+100),self.font, 80, 40)
        self.clock = pygame.time.Clock()
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

class Button:
    def __init__(self, text, center,button_font,button_width,button_height):
        self.text = text
        self.base_rect = pygame.Rect(0, 0, button_width, button_height)
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
            theme=self.menu("CHOOSE A THEME","Phonk","Futuristic","Retro","Space")
            game=self.load(choice,theme)
            winner=game.play()
            pygame.mixer.music.stop()
            pygame.display.set_caption("Mini Game Hub")
            today = date.today()
            with open('history.csv', 'a') as f:
                if winner is None:
                    continue
                if winner=="DRW":
                    f.write(f"{self.p1},{self.p2},{today},{choice},True\n")
                elif winner==self.p1:
                    f.write(f"{self.p1},{self.p2},{today},{choice},False\n")
                else:
                    f.write(f"{self.p2},{self.p1},{today},{choice},False\n")
            while True:
                choice=self.menu("","Leaderboard","Plots","Play again", "Quit")          
                if choice=="Leaderboard":
                    metric=self.menu("METRIC FOR LEADERBOARD","Username","Wins","Win percent","Losses","Loss percent","Wins/Losses")
                    if metric is None:
                        break
                    siz=pygame.display.get_window_size()
                    pos=pygame.display.get_window_position()
                    pygame.display.set_window_position((100,100))
                    self.screen=pygame.display.set_mode((320+30,70+30))
                    subprocess.run(["./leaderboard.sh", metric])
                    btn = Button("PROCEED",(self.screen.get_width()/2,self.screen.get_height()/2),self.button_font,320,70)
                    proceed=False
                    while not proceed:
                        dt=self.clock.tick(fps)/1000
                        mouse_pos=pygame.mouse.get_pos()
                        self.screen.fill((bg_color))
                        btn.draw(mouse_pos,dt,self.screen)
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                proceed=True
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                                    proceed=True
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if btn.pressed(mouse_pos):
                                    proceed=True
                        pygame.display.flip()
                    pygame.display.set_window_position(pos)
                    self.screen=pygame.display.set_mode(siz)
                elif choice=="Plots":
                    self.plotstuff()
                elif choice=="Play again":
                    break
                else :
                    return

    def menu(self,heading,*names):
        button_width=320
        button_height=70
        buttons = []
        for i, name in enumerate(names):
            buttons.append(Button(name,(self.screen.get_width()/2,self.screen.get_height()/2-120+i*100),self.button_font,button_width,button_height))
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

    def load(self,c,theme):
        if c == "Tic-Tac-Toe":
            from games.tictactoe import TicTacToe
            return TicTacToe(self.p1,self.p2,self.screen,theme)
        elif c == "Othello":
            from games.othello import Othello
            return Othello(self.p1,self.p2,self.screen,theme)
        elif c == "Connect4":
            from games.connect4 import Connect4
            return Connect4(self.p1,self.p2,self.screen,theme)
        elif c == "Chain-Reaction":
            from games.chainreaction import ChainRxn
            return ChainRxn(self.p1,self.p2,self.screen,theme)

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
                if field[0] not in totwins:
                    totwins[field[0]]=0
                if field[1] not in totwins:
                    totwins[field[1]]=0
                if field[4] =="False" :
                    totwins[field[0]]+=1
                gameplayfreq[field[3]]+=1
        fontforplottitle = {'family':'serif','color':'blue','size':20}
        choice=self.menu("Which Plot","Top 5 Players","Total Number of wins","Most Played Games","Heat Map of pvp")
        if choice=="Top 5 Players":
            sortedtotwins = sorted(totwins.items(), key=lambda x: x[1], reverse=True)
            top5=[]
            for item in sortedtotwins:
                if len(top5)<5:
                    top5.append(item)
                elif item[1]==top5[4][1]:
                    top5.append(item)
                else:
                    break
            plt.bar([x[0] for x in top5],[x[1] for x in top5])
            plt.title("Top 5 Players",fontdict=fontforplottitle,pad=20)
            plt.ylabel("Total number of wins")
        elif choice=="Total Number of wins":
            plt.pie(list(totwins.values()),labels=list(totwins.keys()))
            plt.title("Total number of wins",fontdict=fontforplottitle,pad=20)
        elif choice=="Most Played Games":
            plt.pie(list(gameplayfreq.values()),labels=list(gameplayfreq.keys()))
            plt.title("Most Played Games",fontdict=fontforplottitle,pad=20)
        elif choice=="Heat Map of pvp":
            winspvp={}
            vmax=0
            vmin=0
            for player1 in totwins:
                winspvp[player1]={}
                for player2 in totwins:
                    winspvp[player1][player2]=0
            with open('history.csv') as f:
                for field in csv.reader(f):
                    if field[4] =="False" :
                        winspvp[field[0]][field[1]]+=1
                        winspvp[field[1]][field[0]]-=1
            for player1 in totwins:
                for player2 in totwins:
                    vmax=max(vmax,winspvp[player1][player2])
                    vmin=min(vmin,winspvp[player1][player2])
            matrixpvp=np.array([[winspvp[player1][player2]for player2 in totwins] for player1 in totwins])
            plt.figure(figsize=(8, 6))
            im = plt.imshow(matrixpvp,origin='lower',cmap='RdBu',vmin=vmin-1,vmax=vmax+1)
            plt.xticks(range(len(totwins.keys())), totwins.keys(),rotation=90)
            plt.xlabel("Player 2")
            plt.yticks(range(len(totwins.keys())), totwins.keys())
            plt.ylabel("Player 1",rotation=90)
            cbar = plt.colorbar(im)
            cbar.set_label("No. of more times 1 has won against 2",rotation=270,labelpad=15)
            plt.title("Heat Map of pvp",fontdict=fontforplottitle,pad=20)
        else:
            return
        plt.tight_layout()
        plt.savefig("plot.png")
        plt.close('all')
        plotimg = pygame.image.load("plot.png")
        subprocess.run(["rm", "plot.png"])
        btn = Button("PROCEED",(self.screen.get_width()/2,self.screen.get_height()-50),self.button_font,320,70)
        while True:
            dt=self.clock.tick(fps)/1000
            mouse_pos=pygame.mouse.get_pos()
            self.screen.fill((255,255,255))
            rect=plotimg.get_rect(center=(self.screen.get_width()/2,self.screen.get_height()/2-60))
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
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()
    player1=sys.argv[1]
    player2=sys.argv[2]
    screen=pygame.display.set_mode(res)
    welcome_font=pygame.font.SysFont("segoeui", 64, bold=True)
    btnplay=Button("Play",(screen.get_width()/2,  screen.get_height()/2+100),welcome_font, 80, 40)
    clock=pygame.time.Clock()
    running=True
    while running:
        dt=clock.tick(60)/1000
        screen.fill((0,0,0))
        title = welcome_font.render("WELCOME", True, (200, 200, 200))
        title = pygame.transform.scale_by(title,1+0.05*np.sin(pygame.time.get_ticks()/200))
        screen.blit(title, title.get_rect(center=(screen.get_width()/2,screen.get_height()/2)))
        btnplay.draw(pygame.mouse.get_pos(),dt,screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btnplay.pressed(pygame.mouse.get_pos()):
                    running=False
        pygame.display.flip()
    engine=GameEngine(player1, player2,screen)
    engine.run()
    stopping=True
    btnbye=Button("Bye",(screen.get_width()/2-100,  screen.get_height()/2+100),welcome_font, 80, 40)
    while stopping:
        dt=clock.tick(60)/1000
        screen.fill((0,0,0))
        title = welcome_font.render("Thanks for playing", True, (200, 200, 200))
        title = pygame.transform.scale_by(title,1+0.05*np.sin(pygame.time.get_ticks()/200))
        screen.blit(title, title.get_rect(center=(screen.get_width()/2,screen.get_height()/2)))
        btnbye.draw(pygame.mouse.get_pos(),dt,screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stopping=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btnbye.pressed(pygame.mouse.get_pos()):
                    stopping=False
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()