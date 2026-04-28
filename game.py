import sys
import numpy as np
import pygame
import matplotlib.pyplot as plt
import csv
from datetime import date
import subprocess

button_color        = (40,40,40)
hover_color         = (70,130,180)
text_color          = (235,235,235)
fps                 = 60

class Game:
    def __init__(self,p1,p2,r,c,screen,theme):
        initbuttonimages()
        self.p1=p1
        self.p2=p2
        self.turn=0
        self.board=np.full((r,c),-1)
        self.r=r
        self.c=c
        self.screen=screen
        self.theme=theme
        self.cell_size=self.cell_size_original
        #pygame.mixer.music.load(f"music/{self.theme}.ogg")
        #pygame.mixer.music.play(-1)
        self.bg_original = pygame.image.load(f"images/{self.theme}.png")
        self.update()
        self.clock = pygame.time.Clock()
        self.quitscreen=False
        self.resultscreen=False
        self.drawclaimed=False
        self.earthquake=True
    def update(self):
        smallerscalevalue=min(self.screen.get_width()/1280, self.screen.get_height()/720)
        self.bg = pygame.transform.scale(self.bg_original, self.screen.get_size())
        self.font = pygame.font.Font("fonts/BlackgothRegular-xRg40.otf", int(36*smallerscalevalue))
        self.btnquityes = Button("Yes",         (self.screen.get_width()*0.43,self.screen.get_height()*0.6),self.font, 80*smallerscalevalue, 80*smallerscalevalue, self.screen)
        self.btnquitno = Button("No",           (self.screen.get_width()*0.57,self.screen.get_height()*0.6),self.font, 80*smallerscalevalue, 80*smallerscalevalue, self.screen)
        self.btnproceedresult =Button("Proceed",(self.screen.get_width()*0.5,self.screen.get_height()*0.7),self.font, 220*smallerscalevalue, 80*smallerscalevalue, self.screen)
        self.btnresign1 = Button("Resign",      (self.screen.get_width()*0.15,self.screen.get_height()*0.55),self.font, 220*smallerscalevalue, 80*smallerscalevalue, self.screen)
        self.btnresign2 = Button("Resign",      (self.screen.get_width()*0.85,self.screen.get_height()*0.55),self.font, 220*smallerscalevalue, 80*smallerscalevalue, self.screen)
        self.btnclaimdraw1=Button("Claim Draw", (self.screen.get_width()*0.15,self.screen.get_height()*0.67),self.font, 220*smallerscalevalue, 80*smallerscalevalue, self.screen)
        self.btnclaimdraw2=Button("Claim Draw", (self.screen.get_width()*0.85,self.screen.get_height()*0.67),self.font, 220*smallerscalevalue, 80*smallerscalevalue, self.screen)
        self.btnacceptdraw=Button("Accept",     (self.screen.get_width()*0.4,self.screen.get_height()*0.6),self.font, 150*smallerscalevalue, 80*smallerscalevalue, self.screen)
        self.btnrejectdraw=Button("Reject",     (self.screen.get_width()*0.6,self.screen.get_height()*0.6),self.font, 150*smallerscalevalue, 80*smallerscalevalue, self.screen)
        self.cell_size=int(self.cell_size_original*smallerscalevalue)
        self.base_pos = pygame.Vector2(self.screen.get_width() / 2 - self.cell_size*self.c/2, self.screen.get_height() / 2 - self.cell_size*self.r/2)
        self.btnpanelp1 = Button("",            (self.screen.get_width()*0.15,self.screen.get_height()*0.53),self.font, 270*smallerscalevalue, 450*smallerscalevalue, self.screen)
        self.btnpanelp2 = Button("",            (self.screen.get_width()*0.85,self.screen.get_height()*0.53),self.font, 270*smallerscalevalue, 450*smallerscalevalue, self.screen)
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
        while True:
            dt = self.clock.tick(fps)/1000
            self.screen.blit(self.bg,(0,0))
            self.drawboard()
            self.btnpanelp1.draw(1-self.turn,dt)
            self.btnpanelp2.draw(self.turn,dt)
            player1=self.font.render(f"{self.p1}", True, (200, 200, 200))
            self.screen.blit(player1, player1.get_rect(center=(self.screen.get_width()*0.15,self.screen.get_height()*0.35)))
            player2=self.font.render(f"{self.p2}", True, (200, 200, 200))
            self.screen.blit(player2, player2.get_rect(center=(self.screen.get_width()*0.85,self.screen.get_height()*0.35)))
            self.btnresign1.draw(self.btnresign1.hoveringonthis(pygame.mouse.get_pos()),dt)
            self.btnresign2.draw(self.btnresign2.hoveringonthis(pygame.mouse.get_pos()),dt)
            self.btnclaimdraw1.draw(self.btnclaimdraw1.hoveringonthis(pygame.mouse.get_pos()),dt)
            self.btnclaimdraw2.draw(self.btnclaimdraw2.hoveringonthis(pygame.mouse.get_pos()),dt)
            if self.quitscreen :
                title=self.font.render("You sure you wanna quit ?", True, (200, 200, 200))
                title = pygame.transform.scale_by(title,1+0.05*np.sin(pygame.time.get_ticks()/200))
                self.screen.blit(title, title.get_rect(center=(self.screen.get_width()/2,self.screen.get_height()*0.4)))
                self.btnquityes.draw(self.btnquityes.hoveringonthis(pygame.mouse.get_pos()),dt)
                self.btnquitno.draw(self.btnquitno.hoveringonthis(pygame.mouse.get_pos()),dt)
            elif self.resultscreen :
                if self.result=="DRW":
                    title=self.font.render("DRAW", True, (200, 200, 200))
                    title = pygame.transform.scale_by(title,1+0.05*np.sin(pygame.time.get_ticks()/200))
                    self.screen.blit(title, title.get_rect(center=(self.screen.get_width()/2,self.screen.get_height()*0.4)))
                else:
                    title=self.font.render(f"WINNER IS {self.result}", True, (200, 200, 200))
                    title = pygame.transform.scale_by(title,1+0.05*np.sin(pygame.time.get_ticks()/200))
                    self.screen.blit(title, title.get_rect(center=(self.screen.get_width()/2,self.screen.get_height()*0.4)))
                self.btnproceedresult.draw(self.btnproceedresult.hoveringonthis(pygame.mouse.get_pos()),dt)
            elif self.drawclaimed:
                title=self.font.render(f"{self.whoclaimdraw} claimed draw", True, (200, 200, 200))
                title = pygame.transform.scale_by(title,1+0.05*np.sin(pygame.time.get_ticks()/200))
                self.screen.blit(title, title.get_rect(center=(self.screen.get_width()/2,self.screen.get_height()*0.4)))
                self.btnacceptdraw.draw(self.btnacceptdraw.hoveringonthis(pygame.mouse.get_pos()),dt)
                self.btnrejectdraw.draw(self.btnrejectdraw.hoveringonthis(pygame.mouse.get_pos()),dt)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quitscreen=True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.quitscreen:
                        if self.btnquityes.hoveringonthis(event.pos):
                            return None
                        elif self.btnquitno.hoveringonthis(event.pos):
                            self.quitscreen=False
                    elif self.resultscreen:
                        if self.btnproceedresult.hoveringonthis(event.pos):
                            return self.result
                    elif self.drawclaimed:
                        if self.btnacceptdraw.hoveringonthis(event.pos):
                            self.result = "DRW"
                            self.resultscreen=True
                        elif self.btnrejectdraw.hoveringonthis(event.pos):
                            self.drawclaimed=False
                    elif self.btnresign1.hoveringonthis(event.pos):
                        self.result = self.p2
                        self.resultscreen = True
                    elif self.btnresign2.hoveringonthis(event.pos):
                        self.result = self.p1
                        self.resultscreen = True
                    elif self.btnclaimdraw1.hoveringonthis(event.pos):
                        self.whoclaimdraw = self.p1
                        self.drawclaimed = True
                    elif self.btnclaimdraw2.hoveringonthis(event.pos):
                        self.whoclaimdraw = self.p2
                        self.drawclaimed = True
                    else:
                        self.specificmousepressevents(event.pos)
                if event.type == pygame.VIDEORESIZE:
                    self.update()
            pygame.display.flip()
    def drawboard(self):
        raise NotImplementedError
    def specificmousepressevents(self,eventpos):
        raise NotImplementedError

class Button:
    img_normal=None
    img_hover=None
    def __init__(self, text, center,button_font,button_width,button_height,screen):
        self.screen = screen
        self.text = text
        self.base_rect = pygame.Rect(0, 0, button_width, button_height)
        self.base_rect.center = center
        self.button_font=button_font
        self.t = 0
        self.rect= self.base_rect.copy()
    def draw(self, hoveronthis, dt):
        if hoveronthis:
            self.t = min(1, self.t + (1-self.t)*10*dt)
        else:
            self.t = max(0, self.t - self.t*10*dt)
        scale = 1 + 0.1 * self.t
        w = int(self.base_rect.width * scale)
        h = int(self.base_rect.height * scale)
        self.rect.size = (w, h)
        self.rect.center = self.base_rect.center
        self.rect.centery-=5*self.t
        img1 = pygame.transform.scale(Button.img_normal, (w, h))
        img2 = pygame.transform.scale(Button.img_hover, (w, h))
        img1.set_alpha(int(255 * (1 - self.t)))
        img2.set_alpha(int(255 * self.t))
        self.screen.blit(img1, self.rect)
        self.screen.blit(img2, self.rect)
        txt = self.button_font.render(self.text.upper(), True, text_color)
        txt_rect = txt.get_rect(center=self.rect.center)
        self.screen.blit(txt, txt_rect)
    def hoveringonthis(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

def initbuttonimages():
    Button.img_normal = pygame.image.load("images/croppedb.png").convert_alpha()
    Button.img_hover  = pygame.image.load("images/croppedu.png").convert_alpha()

class GameEngine:
    def __init__(self,p1,p2,screen,bg):
        initbuttonimages()
        self.p1=p1
        self.p2=p2
        self.screen=screen
        self.title_font=pygame.font.Font("fonts/BlackgothRegular-xRg40.otf", 64)
        self.button_font=pygame.font.Font("fonts/BlackgothRegular-xRg40.otf", 36)
        self.clock = pygame.time.Clock()
        self.bg_original=bg
        self.bg = pygame.transform.scale(self.bg_original,self.screen.get_size())

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
                choice=self.menu("CHOOSE","Leaderboard","Plots","Play again", "Quit")          
                if choice=="Leaderboard":
                    metric=self.menu("METRIC FOR LEADERBOARD","Username","Wins","Win percent","Losses","Loss percent","Wins/Losses")
                    if metric is None:
                        break
                    siz=pygame.display.get_window_size()
                    pos=pygame.display.get_window_position()
                    pygame.display.set_window_position((100,100))
                    self.screen=pygame.display.set_mode((320+30,70+30))
                    subprocess.run(["./leaderboard.sh", metric])
                    btn = Button("PROCEED",(self.screen.get_width()/2,self.screen.get_height()/2),self.button_font,320,70,self.screen)
                    proceed=False
                    while not proceed:
                        dt=self.clock.tick(fps)/1000
                        mouse_pos=pygame.mouse.get_pos()
                        self.screen.fill(((0,0,0)))
                        btn.draw(btn.hoveringonthis(mouse_pos),dt)
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                proceed=True
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                                    proceed=True
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if btn.hoveringonthis(mouse_pos):
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
        smallerscalevalue=min(self.screen.get_width()/1280,self.screen.get_height()/720)
        self.title_font=pygame.font.Font("fonts/BlackgothRegular-xRg40.otf", int(64*smallerscalevalue))
        self.button_font=pygame.font.Font("fonts/BlackgothRegular-xRg40.otf", int(36*smallerscalevalue))
        self.bg = pygame.transform.scale(self.bg_original,self.screen.get_size())
        button_width=320*smallerscalevalue
        button_height=1.4/(5+2*len(names))*self.screen.get_height()
        button_spacing=2/(5+2*len(names))*self.screen.get_height()
        buttons = []
        for i, name in enumerate(names):
            buttons.append(Button(name,(self.screen.get_width()*0.5,self.screen.get_height()*4.7/(5+2*len(names))+i*button_spacing),self.button_font,button_width,button_height,self.screen))
        while True:
            dt=self.clock.tick(fps)/1000
            mouse_pos=pygame.mouse.get_pos()
            self.screen.blit(self.bg,(0,0))
            title = self.title_font.render(heading, True, (200, 200, 200))
            title = pygame.transform.scale_by(title,1.2+0.05*np.sin(pygame.time.get_ticks()/200))
            self.screen.blit(title, title.get_rect(center=(self.screen.get_width()*0.5,self.screen.get_height()*2.5/(5+2*len(names)))))
            for btn in buttons:
                btn.draw(btn.hoveringonthis(mouse_pos),dt)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for btn in buttons:
                        if btn.hoveringonthis(mouse_pos):
                            return btn.text
                if event.type == pygame.VIDEORESIZE:
                    smallerscalevalue=min(self.screen.get_width()/1280,self.screen.get_height()/720)
                    self.title_font=pygame.font.Font("fonts/BlackgothRegular-xRg40.otf", int(64*smallerscalevalue))
                    self.button_font=pygame.font.Font("fonts/BlackgothRegular-xRg40.otf", int(36*smallerscalevalue))
                    self.bg = pygame.transform.scale(self.bg_original,self.screen.get_size())
                    button_width=320*smallerscalevalue
                    button_height=1.4/(5+2*len(names))*self.screen.get_height()
                    button_spacing=2/(5+2*len(names))*self.screen.get_height()
                    buttons = []
                    for i, name in enumerate(names):
                        buttons.append(Button(name,(self.screen.get_width()*0.5,self.screen.get_height()*4.7/(5+2*len(names))+i*button_spacing),self.button_font,button_width,button_height,self.screen))
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
        btn = Button("PROCEED",(self.screen.get_width()*0.5,self.screen.get_height()*0.9),self.button_font,self.screen.get_width()*0.25,self.screen.get_height()*0.1,self.screen)
        while True:
            dt=self.clock.tick(fps)/1000
            mouse_pos=pygame.mouse.get_pos()
            self.screen.fill((255,255,255))
            rect=plotimg.get_rect(center=(self.screen.get_width()*0.5,self.screen.get_height()*0.45))
            self.screen.blit(plotimg, rect)
            btn.draw(btn.hoveringonthis(mouse_pos),dt)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if btn.hoveringonthis(mouse_pos):
                        return
                if event.type == pygame.VIDEORESIZE:
                    btn = Button("PROCEED",(self.screen.get_width()*0.5,self.screen.get_height()*0.9),self.button_font,self.screen.get_width()*0.25,self.screen.get_height()*0.1,self.screen)
            pygame.display.flip()

def main():
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()
    smallerscalevalue=1
    player1=sys.argv[1]
    player2=sys.argv[2]
    screen=pygame.display.set_mode((1280,720),pygame.RESIZABLE)
    clock=pygame.time.Clock()
    bg_original = pygame.image.load("images/Gamehub.png")
    initbuttonimages()

    running=True
    bg = pygame.transform.scale(bg_original, screen.get_size())
    welcome_font=pygame.font.Font("fonts/BlackgothRegular-xRg40.otf", int(64*smallerscalevalue))
    btnpanelwelcome=Button("",(screen.get_width()*0.5,screen.get_height()*0.55),welcome_font, 600*smallerscalevalue, 500*smallerscalevalue, screen)
    btnplay=Button("Play",(screen.get_width()*0.5, screen.get_height()*0.6),welcome_font, 270*smallerscalevalue, 100*smallerscalevalue, screen)
    while running:
        dt=clock.tick(60)/1000
        screen.blit(bg,(0,0))
        btnpanelwelcome.draw(0,dt)
        title = welcome_font.render("WELCOME", True, (200, 200, 200))
        title = pygame.transform.scale_by(title,1.2+0.05*np.sin(pygame.time.get_ticks()/200))
        screen.blit(title, title.get_rect(center=(screen.get_width()*0.5,screen.get_height()*0.4)))
        btnplay.draw(btnplay.hoveringonthis(pygame.mouse.get_pos()),dt)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btnplay.hoveringonthis(pygame.mouse.get_pos()):
                    running=False
            if event.type == pygame.VIDEORESIZE:
                bg = pygame.transform.scale(bg_original, screen.get_size())
                smallerscalevalue=min(screen.get_width()/1280,screen.get_height()/720)
                welcome_font=pygame.font.Font("fonts/BlackgothRegular-xRg40.otf", int(64*smallerscalevalue))
                btnpanelwelcome=Button("",(screen.get_width()*0.5,screen.get_height()*0.5),welcome_font, 330*smallerscalevalue, 600*smallerscalevalue, screen)
                btnplay=Button("Play",(screen.get_width()*0.5, screen.get_height()*0.6),welcome_font, 280*smallerscalevalue, 100*smallerscalevalue, screen)
        pygame.display.flip()

    engine=GameEngine(player1,player2,screen,bg_original)
    engine.run()

    stopping=True
    bg = pygame.transform.scale(bg_original, screen.get_size())
    welcome_font=pygame.font.Font("fonts/BlackgothRegular-xRg40.otf", int(64*smallerscalevalue))
    btnbye=Button("Bye",(screen.get_width()*0.5,  screen.get_height()*0.6),welcome_font, 280*smallerscalevalue, 100*smallerscalevalue, screen)
    while stopping:
        dt=clock.tick(60)/1000
        screen.blit(bg,(0,0))
        title = welcome_font.render("Thanks for playing", True, (200, 200, 200))
        title = pygame.transform.scale_by(title,1.2+0.05*np.sin(pygame.time.get_ticks()/200))
        screen.blit(title, title.get_rect(center=(screen.get_width()*0.5,screen.get_height()*0.4)))
        btnbye.draw(btnbye.hoveringonthis(pygame.mouse.get_pos()),dt)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stopping=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btnbye.hoveringonthis(pygame.mouse.get_pos()):
                    stopping=False
            if event.type == pygame.VIDEORESIZE:
                bg = pygame.transform.scale(bg_original, screen.get_size())
                smallerscalevalue=min(screen.get_width()/1280,screen.get_height()/720)
                welcome_font=pygame.font.Font("fonts/BlackgothRegular-xRg40.otf", int(64*smallerscalevalue))
                btnbye=Button("Bye",(screen.get_width()*0.5, screen.get_height()*0.6),welcome_font, 280*smallerscalevalue, 100*smallerscalevalue, screen)
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()