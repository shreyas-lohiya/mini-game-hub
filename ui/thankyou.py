import pygame
import numpy as np
from ui.button import Button

#the last screen before game finally ends
def thankyouscreen(screen):
    bg_original = pygame.image.load("images/Gamehub.png")
    clock=pygame.time.Clock()
    bg = pygame.transform.scale(bg_original, screen.get_size())
    smallerscalevalue=min(screen.get_width()/1280,screen.get_height()/720)
    welcome_font=pygame.font.Font("fonts/BlackgothRegular-xRg40.otf", int(64*smallerscalevalue))
    btnbye=Button("Bye",(screen.get_width()*0.5,  screen.get_height()*0.6),welcome_font, 280*smallerscalevalue, 100*smallerscalevalue, screen)
    while True:
        dt=clock.tick(60)/1000
        screen.blit(bg,(0,0))
        title = welcome_font.render("Thanks for playing", True, (200, 200, 200))
        title = pygame.transform.scale_by(title,1.2+0.05*np.sin(pygame.time.get_ticks()/200))
        screen.blit(title, title.get_rect(center=(screen.get_width()*0.5,screen.get_height()*0.4)))
        btnbye.draw(btnbye.hoveringonthis(pygame.mouse.get_pos()),dt)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btnbye.hoveringonthis(pygame.mouse.get_pos()):
                    return
            if event.type == pygame.VIDEORESIZE:
                bg = pygame.transform.scale(bg_original, screen.get_size())
                smallerscalevalue=min(screen.get_width()/1280,screen.get_height()/720)
                welcome_font=pygame.font.Font("fonts/BlackgothRegular-xRg40.otf", int(64*smallerscalevalue))
                btnbye=Button("Bye",(screen.get_width()*0.5, screen.get_height()*0.6),welcome_font, 280*smallerscalevalue, 100*smallerscalevalue, screen)
        pygame.display.flip()