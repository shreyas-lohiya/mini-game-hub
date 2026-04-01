import sys
import os
import numpy
import pygame

class Game:
    def __init__(self,p1,p2,r,c):
        self.p=[p1,p2]
        self.turn=0
        self.board=numpy.zeros((r,c))
        self.r=r
        self.c=c
    def current(self):
        return self.p[self.turn]
    def switch_turn(self):
        self.turn=1-self.turn
    def win_check(self):
        raise NotImplementedError
    def draw_check(self):
        raise NotImplementedError
    def valid_check(self):
        raise NotImplementedError
    def move(self,row,col):
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
        
    pygame.quit()


def main():
    player1=sys.argv[1]
    player2=sys.argv[2]
    engine=GameEngine(player1, player2)
    engine.run()

if __name__ == "__main__":
    main()

