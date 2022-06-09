import pygame as pg
import time
import random
import os
from settings import *
from converter import *
from NNpredict import *

class Agent(pg.sprite.Sprite):
    """Class that holds everything for the Agent Character."""
    def __init__(self, game, x, y):
        self.game = game
        self.groups = self.game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)

        self.image = pg.image.load("images/agentx.png").convert_alpha()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.conv = Converter()
        self.current_soil_image = self.game.TILEMAP[self.y][self.x].soil_image
        self.update()

    def move(self, dx=0, dy=0):
        """Moves the position of the player in cartesian coordinates."""
        self.x += dx
        self.y += dy
        self.predictsoil()

    def automove(self, path):
        for move in path:
            (x1, y1) = move
            if x1 != self.x:
                #print(x1-self.x)
                self.move(dx=x1-self.x)
            if y1 != self.y:
                self.move(dy=y1-self.y)
            self.update()
            # Draw updated screen.
            self.game.draw()
            time.sleep(0.3)
    
    def predictsoil(self):
        tile_object = self.game.TILEMAP[self.y][self.x]
        surface_type = NNpredict(tile_object.soil_image_path)
        surface_type = surface_type.tolist()
        surface_type = surface_type[0] #unpack nested list
        
        if surface_type[0] == max(surface_type):
            surface_pred = "Clay"
        if surface_type[1] == max(surface_type):
            surface_pred = "Loam"
        if surface_type[2] == max(surface_type):
            surface_pred = "Sandy Loam"
        if surface_type[3] == max(surface_type):
            surface_pred = "Sandy"

        print("Predicted Soil type: ", surface_pred)
        # Read and display image, PIL library
        print(tile_object.soil_image_path)
        #self.update()
        #self.game.draw() #to move agent visually before opening the soil jpg file
        self.current_soil_image = tile_object.soil_image 
        


    def update(self):
        """Updates the isometric position of the player."""
        self.rect.x, self.rect.y = self.conv.convert_cart(self.x, self.y)

class Tile(pg.sprite.Sprite):
    """All entities that make up the grid background is currently handled in this class."""
    def __init__(self, game, x, y, intsoiltype):
        self.game = game
        self.groups = game.tiles 
        pg.sprite.Sprite.__init__(self, self.groups)

        self.x, self.y = x, y
        self.xy = (self.x, self.y)

        self.intsoiltype = intsoiltype
        self.surface_type = None #buffor, name of surface is being put here later (grass, dirt etc)

        self.soil_image_path = self.choose_soil_image() #filepath to jpg file with soil image
        self.soil_image = pg.image.load(self.soil_image_path) #pygame image of soil

        self.g = None #Entry cost, used for A* (f=g+h), where g is entry cost and h is manhattan distance to end
        self.conv = Converter()
        self.choose_surface_type()

    def choose_soil_image(self):
        if self.intsoiltype == 0:
            dir_filename = "[Clay] Laterite Soil"
        elif self.intsoiltype == 1:
            dir_filename = "[Loamy] Black Soil"
        elif self.intsoiltype == 2:
            dir_filename = "[Sandy Loam] Peat Soil"
        elif self.intsoiltype == 3:
            dir_filename = "[Sandy] Yellow Soil"

        jpg_filename = random.choice(os.listdir(f"""Soil types trainset/{dir_filename}"""))
        jpg_filepath = f"""Soil types trainset/{dir_filename}/{jpg_filename}"""
        return jpg_filepath

    def choose_surface_type(self):
        """Chooses the tile soil, so the image type and entry cost"""
        if self.intsoiltype == 0:
            self.soiltype = "Clay1"
            self.plant = "Carrot"
            self.g = 1
        elif self.intsoiltype == 1:
            self.soiltype = "Loamy1"
            self.plant = "Wheat"
            self.g = 1
        elif self.intsoiltype == 2:
            self.soiltype = "Sandy Loam1"
            self.plant = "Corn1"
            self.g = 1
        elif self.intsoiltype == 3:
            self.soiltype = "Sandy1"
            self.plant = "Sandy1"
            self.g = 20
        self.load_sprite() # Once surface type is chosen, it calls for loading its image
        
        self.load_plant_sprite()


    def load_sprite(self):
        """Loads up choosen sprite image and gets him isometric position"""
        self.image = pg.image.load(f"""images/{self.soiltype}.png""").convert_alpha()
        self.image.set_colorkey(WHITE)#White = transparent
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.conv.convert_cart(self.x, self.y)# Converts cartesian to isometric coordinates

    def load_plant_sprite(self):
        """Loads up choosen sprite image and gets him isometric position"""
        self.plant_image = pg.image.load(f"""images/{self.plant}.png""").convert_alpha()
        self.plant_image.set_colorkey(WHITE)#White = transparent
        self.plant_rect = self.plant_image.get_rect()
        self.plant_rect.x, self.plant_rect.y = self.conv.convert_cart(self.x, self.y)# Converts cartesian to isometric coordinates

    def neighbors(self):
        """Returns list of possible next moves, or possible next coordinates exactly"""
        self.listofneighbors = []
        if self.x+1 <= 19:
            self.listofneighbors.append(self.game.TILEMAP[self.y][self.x+1])#prawy
        if self.x-1 >=0:
            self.listofneighbors.append(self.game.TILEMAP[self.y][self.x-1])#lewy
        if self.y+1 <= 19:
            self.listofneighbors.append(self.game.TILEMAP[self.y+1][self.x])#dolny
        if self.y-1 >=0:     
            self.listofneighbors.append(self.game.TILEMAP[self.y-1][self.x])#gorny
            
        return self.listofneighbors


    def __str__(self):
        return f"""{self.xy}"""

    


        


class Mouseselection(pg.sprite.Sprite):
    """Class that holds everything for the Mouse hovering."""
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load("images/mousex.png").convert_alpha()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.conv = Converter()
        


    def update(self):
        """Updates position of coursor aka highlighted tile."""
        self.mx, self.my = pg.mouse.get_pos()
        self.x, self.y = self.conv.isototilenr(self.mx, self.my)
        self.rect.x, self.rect.y = self.conv.convert_cart(self.x, self.y)

    def click(self):
        """Gets position of clicked tile."""
        self.mx, self.my = pg.mouse.get_pos()
        self.x, self.y = self.conv.isototilenr(self.mx, self.my)
        self.rect.x, self.rect.y = self.conv.convert_cart(self.x, self.y)
        return self.x, self.y