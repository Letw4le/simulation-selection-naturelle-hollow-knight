import pygame



class Button_img():
    def __init__(self, x, y, img, scale,opacity, screen, func_callback):
        image_originale = pygame.image.load(img).convert_alpha()
        self.opacity = opacity
        image_originale.set_alpha(self.opacity)
        width = image_originale.get_width()
        height = image_originale.get_height()
        self.image = pygame.transform.scale(image_originale,(int(width * scale),int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
        self.screen = screen
        self.func_callback = func_callback
        self.activated = False



    def draw_btn(self):

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouse positions and clicked conditions
        if self.rect.collidepoint(pos):
            self.image.set_alpha(255)
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.func_callback()
                self.clicked = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        if self.rect.collidepoint(pos) == False:
            self.image.set_alpha(self.opacity)


        #draw button screen
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

    
    def draw_X2(self):
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouse positions and clicked conditions
        if self.rect.collidepoint(pos):
            self.image.set_alpha(255)
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                if self.activated == False:
                    self.func_callback(2)
                    self.activated = True
                else:
                    self.func_callback(1)
                    self.activated = False
                self.clicked = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        if self.rect.collidepoint(pos) == False and self.activated == False:
            self.image.set_alpha(self.opacity)


        #draw button screen
        self.screen.blit(self.image, (self.rect.x, self.rect.y))






