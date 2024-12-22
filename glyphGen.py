import pygame
import numpy as np
import random
import sys


class GlyphGenerator():
    def __init__(self):

        #pygame display
        pygame.init()

        self.screen_width = 600
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Glyph Generator")
        

        #loading spritesheet
        spritesheetPath = '/Users/frankgallo/Desktop/Programming/glyphGen/radsheet1.png'
        self.spritesheet = pygame.image.load(spritesheetPath).convert_alpha()


        #sprite frame dimensions
        self.sprite_width = 200
        self.sprite_height = 200
        self.locs = 4 #amount of possible variations for each radical minus 1 (used as an array position indicator)

        """
        sprite dict:
            l: left rad
            t: top rad
            b: bottom rad
        """
        self.rad_pos = {
            'l0':(0,0),
            'l1':(0,1),
            'l2':(0, 2),
            'l3':(0, 3),
            'l4':(0, 4),
            't0':(1, 0),
            't1':(1, 1),
            't2':(1, 2),
            't3':(1, 3),
            't4':(1,4),
            'b0':(2,0),
            'b1':(2,1),
            'b2':(2,2),
            'b3':(2,3),
            'b4':(2,4)

        }
    
    def get_sprite(self, row, col):
        """Extract single sprite from sprite sheet"""

        sprite = pygame.Surface((self.sprite_width, self.sprite_height),pygame.SRCALPHA)

        x = col * self.sprite_width
        y = row * self.sprite_height

        #copy specific sprite from the spritesheet
        sprite.blit(self.spritesheet,(0,0),(x,y, self.sprite_width,self.sprite_height))

        return sprite

    def draw_glyph(self):
        #fill the backround
        self.screen.fill((103, 105, 124)) #din gray

        y0 = random.randint(0,self.locs)
        y1 = random.randint(0,self.locs)
        y2 = random.randint(0,self.locs)

        rad0 = f'l{y0}' 
        rad1 = f't{y1}' 
        rad2 = f'b{y2}' 


        #get sprite pos for the radicals
        row0, col0 = self.rad_pos.get(rad0, (0,0)) #default to closed mouth sprite
        row1, col1 = self.rad_pos.get(rad1, (1,0)) #default to closed mouth sprite
        row2, col2 = self.rad_pos.get(rad2, (2,0)) #default to closed mouth sprite

        #get appropriate sprite
        rad0 = self.get_sprite(row0, col0)
        rad1 = self.get_sprite(row1, col1)
        rad2 = self.get_sprite(row2, col2)

        #calculate pos to center the sprite
        sprite_x = (self.screen_width - self.sprite_width) // 2
        sprite_y = (self.screen_height - self.sprite_height) // 2

        #draw sprite to screen
        self.screen.blit(rad0,(sprite_x,sprite_y))
        self.screen.blit(rad1,(sprite_x,sprite_y))
        self.screen.blit(rad2,(sprite_x,sprite_y))

                         
        

        # Update the display
        pygame.display.flip()
    

#main loop
if __name__ == "__main__":
    glyph = GlyphGenerator()
    glyph.draw_glyph()

    print("Glyph Gen")
    print("Enter 'new' for new glyph or 'quit' to exit")

    while True:
        # Handle Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Get input and process it
        writing = input("Selection: ")
        if writing.lower() == 'quit':
            break
        elif writing.lower() == 'new':
            glyph.draw_glyph()
        

    # Cleanup
    pygame.quit()
