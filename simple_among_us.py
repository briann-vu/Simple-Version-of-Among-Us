'''
File: simple_among_us.py
Author: Brian Vu
Purpose: Program displays a very simple and randomized version
    of the video game; 'Among Us'. This game starts with 100
    white circles representing 98 crewmates and two imposters.
    The crewmates can do nothing, but move around the canvas, the
    imposters can 'kill' a crewmate when the two touch. Once an
    imposter reaches 15 kills, their color changes to a light pink
    to indicate that they are 'sus' (suspicious). After 40 kills,
    the imposter's color changes to red which indicates that they
    are an imposter. Once an imposter reaches 45 kills, if they touch
    a crewmate, there is a 50 percent chance for the imposter or crewmate
    to die. If there are only imposters left, imposters win the game and
    vice versa. To start a new game, simply stop the program and run it
    again. The random module and three_shapes_game is imported.
'''

import random
from three_shapes_game import *

def main():
    # This is the size of the window; feel free to tweak it. However,
    # please don’t make this gigantic (about 800x800 should be max),
    # since your TA may not have a screen with crazy-large resolution.
    wid = 400
    hei = 600

    # This creates the Game object. The first param is the window name;
    # the second is the framerate you want (20 frames per second, in this
    # example); the last is the window / game space size.
    game = Game("There Are Two Imposters Among us", 20, wid,hei)

    # This affects how the distance calculation in the "nearby" calls
    # works; the default is to measure center-to-center. But if anybody
    # wants to measure edge-to-edge, they can turn on this feature.
    # game.config_set("account_for_radii_in_dist", True)

    # YOU MUST PROVIDE THIS FUNCTION. This sets up the initial objects
    # that you want to create, at the beginning of the game (if any).
    # Of course, you can remove this is you want to create objects some
    # other way.
    i = 0
    while i < 98:
        spawn_crew(game, wid,hei)
        i += 1
    spawn_imposter(game, wid, hei)
    spawn_imposter(game, wid, hei)

    # game loop. Runs forever, unless the game ends.
    count = 0
    while not game.is_over():
        game.do_nearby_calls()
        game.do_move_calls()
        game.do_edge_calls()
        game.execute_removes()
        game.draw()

        # YOU MUST PROVIDE THIS FUNCTION (or remove this call). This
        # allows you to spawn additional objects over time. It is
        # called once per game tick.


def spawn_crew(game, wid, hei):
    '''
    Function creates a crewmate object and adds it to the
    game object

    game: game object
    wid: int representing the width of the canvas
    hei: int representing the height of the canvas
    '''
    crew_mate = Crew_Mate(wid, hei)
    game.add_obj(crew_mate)


def spawn_imposter(game, wid, hei):
    '''
    Function creates an imposter object and adds it to the
    game object

    game: game object
    wid: int representing the width of the canvas
    hei: int representing the height of the canvas
    '''
    imposter = Imposter(wid, hei)
    game.add_obj(imposter)

class Crew_Mate:
    '''
    This class represents crewmates and what they are allowed
    to do and when they are allowed to do so.

    The constructor builds a crewmate; the crewmate is represented
    by a circle and the color white with the size of 20. The crewmate
    also spawns in random areas of the canvas.

    Methods:
        get_xy: gettors for the coordinates of the object
        get_radius: gettors for the radius of the object
        nearby: allows interactions between two objects that are nearby
        move: determines what direction the object will move across the campus
        edge: determines the direction of movement for the object based on
        which edge it's near.
        draw: draws the object onto the canvas
    '''
    def __init__(self, wid, hei):
        self.x = random.randint(0,wid)
        self.y = random.randint(0, hei)
        self.diameter = 20
        self.color = 'white'
        self.number = random.randint(1,8)

    def get_xy(self):
        return (self.x, self.y)

    def get_radius(self):
        return self.diameter / 2

    def nearby(self, other, dist, game):
        if dist <= 20:
            if isinstance(other, Imposter):
                if other.kills >= 45:
                    #  at this point, crewmates have a chance to kill imposters
                    num = random.randint(1,2)
                    if num == 1:
                        game.remove_obj(other)
                    else:
                        game.remove_obj(self)

    def move(self, game):
        if self.number == 1:
            self.y -= 10
        elif self.number == 2:
            self.x += 10
            self.y -= 10
        elif self.number == 3:
            self.x += 10
        elif self.number == 4:
            self.x += 10
            self.y += 10
        elif self.number == 5:
            self.y += 10
        elif self.number == 6:
            self.x -= 10
            self.y += 10
        elif self.number == 7:
            self.x -= 10
        elif self.number == 8:
            self.x -= 10
            self.y -= 10


    def edge(self, dirr, position):
        if dirr == 'top':
            if position == 0:
                self.number = random.randint(3, 7)
        elif dirr == 'left':
            if position == 0:
                self.number = random.randint(1, 5)
        elif dirr == 'bottom':
            if position == 600:
                self.number = random.choice([1,2,3,7,8])
        elif dirr == 'right':
            if position == 400:
                self.number = random.choice([1, 5, 6, 7, 8])

    def draw(self, win):
        win.ellipse(self.x, self.y, self.diameter, self.diameter, self.color)

class Imposter:
    '''
    This class represents imposters and how they change and how they
    interact with the crewmates.

    The constructor builds an imposter; the imposter is represented
    by a circle and the color white with the size of 20. The imposteer
    also spawns in random areas of the canvas.

    Methods:
        get_xy: gettors for the coordinates of the object
        get_radius: gettors for the radius of the object
        nearby: allows interactions between two objects that are nearby
        move: determines what direction the object will move across the campus
        edge: determines the direction of movement for the object based on
        which edge it's near.
        draw: draws the object onto the canvas
    '''
    def __init__(self, wid, hei):
        self.x = random.randint(0,wid)
        self.y = random.randint(0, hei)
        self.diameter = 20
        self.color = 'white'
        self.number = random.randint(1,8)
        self.kills = 0

    def get_xy(self):
        return (self.x, self.y)

    def get_radius(self):
        return self.diameter / 2

    def nearby(self, other, dist, game):
        if dist <= 20:
            if isinstance(other, Crew_Mate):
                if self.kills < 40:
                    #  at this point the imposter is free to kill as much as possible
                    game.remove_obj(other)
                    self.kills += 1
                    if self.kills >= 15:
                        self.color = '#FFB6C1'
                        #  imposter turns pink to indicate they're suspicious
                else:
                    self.color = 'red'
                    #  imposter turns red after 40 kills
                    game.remove_obj(other)
                    self.kills += 1


    def move(self, game):
        if self.number == 1:
            self.y -= 10
        elif self.number == 2:
            self.x += 10
            self.y -= 10
        elif self.number == 3:
            self.x += 10
        elif self.number == 4:
            self.x += 10
            self.y += 10
        elif self.number == 5:
            self.y += 10
        elif self.number == 6:
            self.x -= 10
            self.y += 10
        elif self.number == 7:
            self.x -= 10
        elif self.number == 8:
            self.x -= 10
            self.y -= 10


    def edge(self, dirr, position):
        if dirr == 'top':
            if position == 0:
                self.number = random.randint(3, 7)
        elif dirr == 'left':
            if position == 0:
                self.number = random.randint(1, 5)
        elif dirr == 'bottom':
            if position == 600:
                self.number = random.choice([1,2,3,7,8])
        elif dirr == 'right':
            if position == 400:
                self.number = random.choice([1, 5, 6, 7, 8])

    def draw(self, win):
        win.ellipse(self.x, self.y, self.diameter, self.diameter, self.color)



if __name__ == "__main__":
    main()