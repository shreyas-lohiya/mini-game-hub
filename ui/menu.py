import pygame
from ui.button import Button
import numpy as np

fps=60 

#displays a menu with buttons from which you can choose an option
#heading and options are passed as an argument and it automatically calculates required heights depending on the number of options
def menu(screen,heading,*options):
    bg_original = pygame.image.load("images/Gamehub.png")
    clock = pygame.time.Clock()
    smallerscalevalue=min(screen.get_width()/1280,screen.get_height()/720)
    title_font=pygame.font.Font("fonts/BlackgothRegular-xRg40.otf", int(64*smallerscalevalue))
    button_font=pygame.font.Font("fonts/BlackgothRegular-xRg40.otf", int(36*smallerscalevalue))
    bg = pygame.transform.scale(bg_original,screen.get_size())
    button_width=320*smallerscalevalue
    button_height=1.4/(5+2*len(options))*screen.get_height()
    button_spacing=2/(5+2*len(options))*screen.get_height()
    
    buttons = []
    for i, name in enumerate(options):
        buttons.append(Button(name,(screen.get_width()*0.5,screen.get_height()*4.7/(5+2*len(options))+i*button_spacing),button_font,button_width,button_height,screen))
    
    while True:
        dt=clock.tick(fps)/1000
        mouse_pos=pygame.mouse.get_pos()
        screen.blit(bg,(0,0))
        title = title_font.render(heading, True, (200, 200, 200))
        title = pygame.transform.scale_by(title,1.2+0.05*np.sin(pygame.time.get_ticks()/200))
        screen.blit(title, title.get_rect(center=(screen.get_width()*0.5,screen.get_height()*2.5/(5+2*len(options)))))
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
                smallerscalevalue=min(screen.get_width()/1280,screen.get_height()/720)
                title_font=pygame.font.Font("fonts/BlackgothRegular-xRg40.otf", int(64*smallerscalevalue))
                button_font=pygame.font.Font("fonts/BlackgothRegular-xRg40.otf", int(36*smallerscalevalue))
                bg = pygame.transform.scale(bg_original,screen.get_size())
                button_width=320*smallerscalevalue
                button_height=1.4/(5+2*len(options))*screen.get_height()
                button_spacing=2/(5+2*len(options))*screen.get_height()
                buttons = []
                for i, name in enumerate(options):
                    buttons.append(Button(name,(screen.get_width()*0.5,screen.get_height()*4.7/(5+2*len(options))+i*button_spacing),button_font,button_width,button_height,screen))
        pygame.display.flip()
