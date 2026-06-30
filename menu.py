import pygame

class Button():
    def __init__(self, x, y, txt, screen, func_callback, centrer=False):
        self.txt = txt
        self.screen = screen
        self.func_callback = func_callback
        self.clicked = False

        font = pygame.font.SysFont("timesnewroman", 30)
        
        # Créer la surface du texte
        self.text_surface = font.render(txt, True, (255, 255, 255))
        
        # La taille du bouton s'adapte au texte + padding
        padding_x, padding_y = 20, 10
        width = self.text_surface.get_width() + padding_x * 2
        height = self.text_surface.get_height() + padding_y * 2
        
        self.rect = pygame.Rect(x, y, width, height)

        if centrer:
            self.rect.centerx = screen.get_width() // 2
        else:
            self.rect.x = x

        # Position du texte centré dans le bouton
        self.text_pos = (self.rect.x + padding_x, self.rect.y + padding_y)



    def draw(self):
        pos = pygame.mouse.get_pos()
        
        # Changer la couleur au survol
        if self.rect.collidepoint(pos):
            couleur_fond = (60, 60, 60)   # gris foncé au survol
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                self.func_callback()
        else:
            couleur_fond = (30, 30, 30)   # gris très foncé par défaut

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Dessiner fond + bordure + texte
        pygame.draw.rect(self.screen, couleur_fond, self.rect, border_radius=8)
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect, width=2, border_radius=8)
        self.screen.blit(self.text_surface, self.text_pos)