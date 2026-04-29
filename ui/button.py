import pygame

#color of the text in button
text_color          = (235,235,235)

#function to initialise button images
def initbuttonimages():
    Button.img_normal = pygame.image.load("images/croppedb.png").convert_alpha()
    Button.img_hover  = pygame.image.load("images/croppedu.png").convert_alpha()

#has objects as hoverable buttons
class Button:
    img_normal=None
    img_hover=None
    def __init__(self, text, center,button_font,button_width,button_height,screen):
        self.screen = screen
        self.text = text
        self.base_rect = pygame.Rect(center[0]-button_width/2, center[1]-button_height/2, button_width, button_height)
        self.base_rect
        self.button_font=button_font
        self.t = 0  #variable that stores progress of the hover from 0 to not touching and 1 to fully hovered
        self.rect= self.base_rect.copy()
        
    #if isithovering is true it is being hovered, else not
    def draw(self, isithovering, dt):
        if isithovering:
            self.t = min(1, self.t + (1-self.t)*10*dt)
        else:
            self.t = max(0, self.t - self.t*10*dt)
        scale = 1 + 0.1 * self.t #makes the button big on hover
        w = int(self.base_rect.width * scale)
        h = int(self.base_rect.height * scale)
        self.rect.size = (w, h)
        self.rect.center = self.base_rect.center
        self.rect.centery-=5*self.t #raises the button on hover
        img1 = pygame.transform.scale(Button.img_normal, (w, h))
        img2 = pygame.transform.scale(Button.img_hover, (w, h))
        img1.set_alpha(int(255 * (1 - self.t))) #first image becomes more transparent as hover is progressed
        img2.set_alpha(int(255 * self.t)) #second image becomes less transparent as hover is progressee
        self.screen.blit(img1, self.rect)
        self.screen.blit(img2, self.rect)
        txt = self.button_font.render(self.text.upper(), True, text_color)
        txt_rect = txt.get_rect(center=self.rect.center)
        self.screen.blit(txt, txt_rect)
        
    #returns whether mouse is on this or not
    def hoveringonthis(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)