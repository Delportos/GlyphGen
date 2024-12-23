import pygame
import numpy as np
import random
import sys
import os


class GlyphGenerator():
    def __init__(self):

        #pygame display
        pygame.init()

        self.screen_width = 600
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Glyph Generator")
        
        # getting current script's directory
        current_dir = os.path.dirname(__file__)

        # build the relative path
        spritesheetPath = os.path.join(current_dir, 'radsheet1.png')

        #loading spritesheet
        self.spritesheet = pygame.image.load(spritesheetPath).convert_alpha()


        #sprite frame dimensions
        self.sprite_width = 200
        self.sprite_height = 200
        self.locs = 4 #amount of possible variations for each radical minus 1 (used as an array position indicator)
        self.current_size = (200,200)
        
        """
        sprite dict:
            l: left rad
            t: top rad
            b: bottom rad
        """
        self.rad_pos = {
            'l0':(0,0), 'l1':(0,1),'l2':(0, 2), 'l3':(0, 3), 'l4':(0, 4),
            't0':(1, 0), 't1':(1, 1), 't2':(1, 2),'t3':(1, 3),'t4':(1,4),
            'b0':(2,0),'b1':(2,1),'b2':(2,2),'b3':(2,3), 'b4':(2,4)

        }
    
    def get_sprite(self, row, col, target_size=None):
        """
        Extract and optionally size a single sprite from sprite sheet

        Args:
            row(int): Row number in spritesheet
            col(int): Column number in spritesheet
            target_size(tuple): Optional(width,height) for resizing
        """

        sprite = pygame.Surface((self.sprite_width, self.sprite_height),pygame.SRCALPHA)

        x = col * self.sprite_width
        y = row * self.sprite_height

        #copy specific sprite from the spritesheet
        sprite.blit(self.spritesheet,(0,0),(x,y, self.sprite_width,self.sprite_height))

        #resize the sprite if the target size is specified
        if target_size:
            sprite = pygame.transform.scale(sprite, target_size)

        return sprite

    def draw_glyph(self, size=None):

        """
        draw glyph with specified size

        args:
            size(tuple): (width, height) of the output glyph
        """

        if size is None:
            size = self.current_size
        else:
            self.current_size = size
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
        rad0 = self.get_sprite(row0, col0, size)
        rad1 = self.get_sprite(row1, col1, size)
        rad2 = self.get_sprite(row2, col2, size)

        #calculate pos to center the sprite
        sprite_x = (self.screen_width - size[0]) // 2
        sprite_y = (self.screen_height - size[1]) // 2

        #draw sprite to screen
        self.screen.blit(rad0,(sprite_x,sprite_y))
        self.screen.blit(rad1,(sprite_x,sprite_y))
        self.screen.blit(rad2,(sprite_x,sprite_y))

                         
        # Update the display
        pygame.display.flip()
    
    def character_gen(self,char_amount):
        characters = []
        attempts = 0 #avoids infinite loops
        maxattempts = 1000
        

        while len(characters) < char_amount and attempts < maxattempts:
            y0 = random.randint(0,self.locs)
            y1 = random.randint(0,self.locs)
            y2 = random.randint(0,self.locs)
            new_character = (f'l{y0}',f't{y1}',f'b{y2}')

            if new_character not in characters:
                characters.append(new_character)

            attempts += 1
        return characters
    def draw_glyph_at_pos(self, rad_tuple, position, size=(100,100)):
        """Draw a single glyph at a specified position"""
        rad0, rad1, rad2 = rad_tuple

        # get sprite positons for the radicals
        row0, col0 = self.rad_pos.get(rad0,(0,0))
        row1, col1 = self.rad_pos.get(rad1,(1,0))
        row2, col2 = self.rad_pos.get(rad2,(2,0))


        # get sprites
        sprite0 = self.get_sprite(row0,col0,size)
        sprite1 = self.get_sprite(row1,col1,size)
        sprite2 = self.get_sprite(row2,col2,size)

        #draw sprites at specified position
        self.screen.blit(sprite0, position)
        self.screen.blit(sprite1, position)
        self.screen.blit(sprite2, position)


    def draw_glyph_grid(self, amount, out, num_glyphs=15):
        """Draw a grid of random glyphs from the unique set"""
        # generate unique characters
        characters = self.character_gen(amount)
        selected_chars = [random.choice(characters) for _ in range(out)]  #


        #clear screen
        self.screen.fill((103,105,124))

        # grid settings

        glyph_size = 100
        glyphs_per_row = 6
        margin_x = (self.screen_width - (glyphs_per_row * glyph_size)) // 2 # (// is floor div)
        margin_y = 50 # Top margin
        spacing = 0 #additional spacing between glyphs if needed

        #draw glyphs in grid
        for i, current_char in enumerate(selected_chars):
            #calculate row and column
            row = i // glyphs_per_row #(floor div)
            col = i % glyphs_per_row

            #calculate positon
            x = margin_x + (col * (glyph_size + spacing))
            y = margin_y + (row * (glyph_size + spacing))

            # draw glyph
            self.draw_glyph_at_pos(current_char,(x,y),(glyph_size,glyph_size))

        pygame.display.flip()

#main loop
if __name__ == "__main__":
    glyph = GlyphGenerator()
    print(glyph.character_gen(15))
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
        elif writing.lower() == 'grid':
            glyph.draw_glyph_grid(15,30)
        elif writing.lower() == 'size':
            try:
                size_input = input("Glyph Size:")
                size = int(size_input)
                if size < 50:
                    print("Size too small. Using min size of 50")
                elif size > 600: 
                    print("Size too large, using max size of 600")
                glyph.draw_glyph(size=(size, size))
            except ValueError:
                print("Invalid size. Using default size of 200")
                glyph.draw_glyph(size=(size, size))

    # Cleanup
    pygame.quit()
