import sys
import numpy as np
import pygame
import matplotlib.pyplot as plt
import csv
from datetime import date
import subprocess
from games.tictactoe import TicTacToe
from games.othello import Othello
from games.connect4 import Connect4
from games.chainreaction import ChainRxn
from ui.button import Button,initbuttonimages
from ui.menu import menu
from ui.welcome import welcomescreen
from ui.thankyou import thankyouscreen

text_color          = (235,235,235)
fps                 = 60

#class that handles the overall game hub except for the part in between choosing a game and quitting that game
class GameEngine:
    #initalises button images, player names, screen, fonts, clock
    def __init__(self,p1,p2,screen):
        initbuttonimages()
        self.p1=p1
        self.p2=p2
        self.screen=screen
        self.title_font=pygame.font.Font("fonts/BlackgothRegular-xRg40.otf", 64)
        self.button_font=pygame.font.Font("fonts/BlackgothRegular-xRg40.otf", 36)
        self.clock = pygame.time.Clock()

    #main loop
    def run(self):
        pygame.display.set_caption("Mini Game Hub")
        
        #keeps asking for which game to play,
        #continue anywhere works as a way to coe back to this screen,
        #break triggers the end of game play and thankyou screen
        while True:
            #choosing game
            choice=menu(self.screen,"CHOOSE A GAME","Tic-Tac-Toe", "Othello", "Connect4", "Chain-Reaction")
            if choice is None: #player quits the game selection screen
                return
            
            #choosing theme
            theme=menu(self.screen,"CHOOSE A THEME","Phonk","Futuristic","Retro","Space")
            if theme is None: #player quits the theme selection screen
                continue
            
            #loads the game plays that specific game and stores winner(or result), then stops the music started by the game, resets the caption changed by the game
            game=self.load(choice,theme)
            winner=game.play()
            pygame.mixer.music.stop()
            pygame.display.set_caption("Mini Game Hub")
            
            #store data in history.csv, 5th field is true when it is draw, then 1st and 2nd field could be in any order
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
                    
            #after the game it goes into an endless loop of asking whether to see plots or leaderboard,
            #stopping only if player quits or wants to play again
            while True:
                choice=menu(self.screen,"CHOOSE","Leaderboard","Plots","Play again", "Quit")   
                if choice=="Leaderboard":
                    self.leaderboard()
                elif choice=="Plots":
                    self.plotstuff()
                elif choice=="Play again":
                    break
                else :
                    return
    
    #loads the game     
    def load(self,c,theme):
        if c == "Tic-Tac-Toe":
            return TicTacToe(self.p1,self.p2,self.screen,theme)
        elif c == "Othello":
            return Othello(self.p1,self.p2,self.screen,theme)
        elif c == "Connect4":
            return Connect4(self.p1,self.p2,self.screen,theme)
        elif c == "Chain-Reaction":
            return ChainRxn(self.p1,self.p2,self.screen,theme)
    
    #shows leaderboard
    def leaderboard(self):
        #asks for metric
        metric=menu(self.screen,"METRIC FOR LEADERBOARD","Username","Wins","Win percent","Losses","Loss percent","Wins/Losses")
        if metric is None: #player didnt select any metric
            return
        
        #move the pygame window to top rght corner and shorten it
        siz=pygame.display.get_window_size()
        pos=pygame.display.get_window_position()
        pygame.display.set_window_position((100,100))
        self.screen=pygame.display.set_mode((320+30,70+30))
        
        #run leaderboard with metric while displaying a proceed button on the top right corner
        subprocess.run(["./leaderboard.sh", metric])
        btn = Button("PROCEED",(self.screen.get_width()/2,self.screen.get_height()/2),self.button_font,320,70,self.screen)
        
        #looop that stops when proceed clicked
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
            
        #resets the window to where it was
        pygame.display.set_window_position(pos)
        self.screen=pygame.display.set_mode(siz)
    
    #shows matplotlib  
    def plotstuff(self):
        #reading the data
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
                
        #selecting font
        fontforplottitle = {'family':'serif','color':'blue','size':20}
        
        #display whatever plot he chooses, function returns None if he quits
        choice=menu(self.screen,"Which Plot","Top 5 Players","Total Number of wins","Most Played Games","Heat Map of pvp")
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
        
        #saves the image into plot.png which is later loaded into pygame and then removed from the memory
        plt.tight_layout()
        plt.savefig("plot.png")
        plt.close('all')
        plotimg = pygame.image.load("plot.png")
        subprocess.run(["rm", "plot.png"])
        
        #displays the plot with a proceed button
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

#############################
######## MAIN CODE ##########
#############################
def main():
    #intitalises pygame and inputs player names from arguments
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()
    player1=sys.argv[1]
    player2=sys.argv[2]
    
    #sets screen loads button images and shows welcome screen, runs game, then shows thankyou screen, ending with pygame.quit
    screen=pygame.display.set_mode((1280,720),pygame.RESIZABLE)
    initbuttonimages()
    if welcomescreen(screen):
        engine=GameEngine(player1,player2,screen)
        engine.run()
    thankyouscreen()
    pygame.quit()
    
if __name__ == "__main__":
    main()