import numpy as np
import pygame 
from ui.button import Button,initbuttonimages

fps=60

class Game:
    #sets player names, whose turn, no. of row, cols, intial board, screen, background,cell,piece radius in original size, button images,things that get updated on screen resize, clock, music, and special screens related variables 
    def __init__(self,p1,p2,r,c,cell_size_original,piece_radius_original,screen,theme,boardshaking):
        self.p1=p1
        self.p2=p2
        self.turn=0
        self.r=r
        self.c=c
        self.board=np.full((r,c),-1)
        self.screen=screen
        self.bg_original = pygame.image.load(f"images/{theme}.png")
        self.cell_size_original = cell_size_original
        self.piece_radius_original = piece_radius_original
        initbuttonimages()
        self.update()
        self.clock = pygame.time.Clock()
        pygame.mixer.music.load(f"audio/{theme}.ogg")
        pygame.mixer.music.play(-1)
        self.quitscreen=False
        self.resultscreen=False
        self.drawclaimed=False
        self.boardshaking=boardshaking
        
    #sets things that are updated on resizing the board
    def update(self):
        #smaller of the scaling value among width scaling vs height scaling
        smallerscalevalue=min(self.screen.get_width()/1280, self.screen.get_height()/720)
        
        self.cell_size=int(self.cell_size_original*smallerscalevalue)
        self.piece_radius=int(self.piece_radius_original*smallerscalevalue)
        self.mean_pos = pygame.Vector2(self.screen.get_width() / 2 - self.cell_size*self.c/2, self.screen.get_height() / 2 - self.cell_size*self.r/2)
        self.base_pos = self.mean_pos.copy()
        self.bg = pygame.transform.scale(self.bg_original, self.screen.get_size())
        #self.token1 = pygame.transform.scale(self.token1_original, (20*smallerscalevalue,20*smallerscalevalue))
        #self.token2 = pygame.transform.scale(self.token2_original, (20*smallerscalevalue,20*smallerscalevalue))
        
        self.font = pygame.font.Font("fonts/BlackgothRegular-xRg40.otf", int(36*smallerscalevalue))
        self.btnquityes =     Button("Yes",       (self.screen.get_width()*0.43,self.screen.get_height()*0.60),self.font,  80*smallerscalevalue,  80*smallerscalevalue, self.screen)
        self.btnquitno =      Button("No",        (self.screen.get_width()*0.57,self.screen.get_height()*0.60),self.font,  80*smallerscalevalue,  80*smallerscalevalue, self.screen)
        self.btnproceedresult=Button("Proceed",   (self.screen.get_width()*0.50,self.screen.get_height()*0.70),self.font, 220*smallerscalevalue,  80*smallerscalevalue, self.screen)
        self.btnresign1 =     Button("Resign",    (self.screen.get_width()*0.15,self.screen.get_height()*0.55),self.font, 220*smallerscalevalue,  80*smallerscalevalue, self.screen)
        self.btnresign2 =     Button("Resign",    (self.screen.get_width()*0.85,self.screen.get_height()*0.55),self.font, 220*smallerscalevalue,  80*smallerscalevalue, self.screen)
        self.btnclaimdraw1 =  Button("Claim Draw",(self.screen.get_width()*0.15,self.screen.get_height()*0.67),self.font, 220*smallerscalevalue,  80*smallerscalevalue, self.screen)
        self.btnclaimdraw2 =  Button("Claim Draw",(self.screen.get_width()*0.85,self.screen.get_height()*0.67),self.font, 220*smallerscalevalue,  80*smallerscalevalue, self.screen)
        self.btnacceptdraw =  Button("Accept",    (self.screen.get_width()*0.40,self.screen.get_height()*0.60),self.font, 150*smallerscalevalue,  80*smallerscalevalue, self.screen)
        self.btnrejectdraw =  Button("Reject",    (self.screen.get_width()*0.60,self.screen.get_height()*0.60),self.font, 150*smallerscalevalue,  80*smallerscalevalue, self.screen)
        self.btnpanelp1 =     Button("",          (self.screen.get_width()*0.15,self.screen.get_height()*0.53),self.font, 270*smallerscalevalue, 450*smallerscalevalue, self.screen)
        self.btnpanelp2 =     Button("",          (self.screen.get_width()*0.85,self.screen.get_height()*0.53),self.font, 270*smallerscalevalue, 450*smallerscalevalue, self.screen)
    
    #function to switch turn
    def switch_turn(self):
        self.turn=1-self.turn
        
    #function to check win
    def win_check(self,i,j):
        raise NotImplementedError
    
    #function to check draw
    def draw_check(self):
        raise NotImplementedError
    
    #function to check if move is valid
    def valid_check(self,i,j):
        raise NotImplementedError
    
    #updates board according to move
    def move(self,i,j):
        raise NotImplementedError
    
    #draws the board along with pieces and animation
    def drawboard(self):
        raise NotImplementedError
    
    #does the necessary checks after a mouse press event that are specific to that game
    def specificmousepressevents(self,eventpos):
        raise NotImplementedError
    
    #main game loop
    def play(self):
        while True:
            #set time and draw backgound
            dt = self.clock.tick(fps)/1000
            self.screen.blit(self.bg,(0,0))
            
            #draw board along with various buttons and player names
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
            
            #draw special evets specific things
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
                
            #event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quitscreen=True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
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
                    
            #code so that you can move the whole board with wasd 
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] or keys[pygame.K_UP] :
                self.mean_pos.y -= 300 * dt
                self.base_pos.y -= 300 * dt
            if keys[pygame.K_s] or keys[pygame.K_DOWN] :
                self.mean_pos.y += 300 * dt
                self.base_pos.y += 300 * dt
            if keys[pygame.K_a] or keys[pygame.K_LEFT] :
                self.mean_pos.x -= 300 * dt
                self.base_pos.x -= 300 * dt
            if keys[pygame.K_d] or keys[pygame.K_RIGHT] :
                self.mean_pos.x += 300 * dt
                self.base_pos.x += 300 * dt
                
            #code for shaking the board
            if self.boardshaking :
                randx=2*np.random.rand()-1
                randy=2*np.random.rand()-1
                self.base_pos.x = self.mean_pos.x + 600 * dt * randx
                self.base_pos.y = self.mean_pos.y + 600 * dt * randy
                
            #flipping the baord finally
            pygame.display.flip()