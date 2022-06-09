import pygame as pg
import random
import threading
import time
import sys
from settings import *
from converter import *
from tiles import *
from astarv1 import *
from GENETIC import genetic_mapmaker


class Game:

    def __init__(self):
        """Initialize screen, pygame, and settings."""
        pg.init()
        self.screen = pg.display.set_mode((1200, 600), 0, 32)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.TILEMAP = []
        self.conv = Converter()
        self.interval = 5


    def new(self):
        """Initialize all variables and do all the setup for a new game."""
        self.all_sprites = pg.sprite.Group()
        self.tiles = pg.sprite.Group() #two grouops of Tiles, just for simplier management
        self.intsoilmap = genetic_mapmaker()
        for y in range(20):
            self.tmbuff=[]
            for x in range(20):
                s = self.intsoilmap[y][x]
                self.tmbuff.append(Tile(self, x, y, intsoiltype=s)) #single row of TILEMAP
            self.TILEMAP.append(self.tmbuff) #TILEMAP (holds 20x20 Tile objects)

        for row in self.TILEMAP:
            for tile in row:
                print(tile.g, end=" ")
            print("\n")
        
        self.agent = Agent(self, 0, 0)
        self.mouse = Mouseselection(self, 1, 1)
        #print(self.TILEMAP[2][2].neighbors())
        #print(a_star_search(self.TILEMAP[self.agent.y][self.agent.x], self.TILEMAP[4][6]))


        

    def draw(self):
        """Draw the screen."""
        self.screen.fill(BGCOLOR)
        for tile in self.tiles:
            self.screen.blit(tile.image, tile.rect)
            self.screen.blit(tile.plant_image, tile.plant_rect)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, sprite.rect)
            
        self.screen.blit(self.agent.current_soil_image, (0,0))

        pg.display.flip()

    def events(self):
        """Catch all events here."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_LEFT:
                    self.agent.move(dx=-1)
                if event.key == pg.K_RIGHT:
                    self.agent.move(dx=1)
                if event.key == pg.K_UP:
                    self.agent.move(dy=-1)
                if event.key == pg.K_DOWN:
                    self.agent.move(dy=1)
            if event.type == pg.MOUSEBUTTONDOWN:
                print(self.mouse.click())
                path = a_star_search(self.TILEMAP[self.agent.y][self.agent.x], self.TILEMAP[self.mouse.y][self.mouse.x])
                print(path)
                self.agent.automove(path)
                    

    def quit(self):
        """Quit the game."""
        pg.quit()
        sys.exit()
    
    def run(self):
        """Game loop."""
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            # Catch all events.
            self.events()
            # Update data.
            #self.update()
            self.mouse.update()
            self.all_sprites.update()
            # Draw updated screen.
            self.draw()


# Create game object.
g = Game()
while True:
    g.new()
    # Main Game Loop
    g.run()



###a star na przestrzeni stanow, heurestyka odleglosc manhattan, koszt pola 