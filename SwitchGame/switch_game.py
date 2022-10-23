""" A Switch Puzzle
10/16/2022
by jhnh198, https://github.com/jhnh198
Uses references from Tech With Tim, techwithtim.net pygame tutorials.
Image and audio assets are from Kenney Free Assets:  Kenney.nl.assets

The object of the game is to hit the switches in the right order to solve the puzzle
The switches have two properties; a number and a color
When the player hits the switch, either the correct number in the sequence or the correct color is valid, but not both
Each switch can solve 1 part of the puzzle sequence.

At the beginning diffculty of the game, the switches properties will change at slow random intervals.
In harder stages of the game, the switches, numbers and tile will change to random values more frequently as well as
having unsolved puzzle pieces change tiles.

"""
import random
import sys
import pygame
import os

pygame.init()


win = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Switch Puzzle")

intro_png = pygame.image.load(os.path.join("images", "explanation.png"))
victory_png = pygame.image.load(os.path.join("images", "victory.png"))

player_png = pygame.image.load(os.path.join("images", "blob.png"))
player_png = pygame.transform.scale(player_png, (36, 36))

switch_left_png = pygame.image.load(os.path.join("images", "switch_left.png"))
switch_right_png = pygame.image.load(os.path.join("images", "switch_right.png"))

switch_left_png = pygame.transform.scale(switch_left_png, (36, 36))
switch_right_png = pygame.transform.scale(switch_right_png, (36, 36))

circle_green_png = pygame.image.load(os.path.join("images", "circle_green.png"))
circle_red_png = pygame.image.load(os.path.join("images", "circle_red.png"))

tile_blue_png = pygame.image.load(os.path.join("images", "tile_blue.png"))
tile_green_png = pygame.image.load(os.path.join("images", "tile_green.png"))
tile_red_png = pygame.image.load(os.path.join("images", "tile_red.png"))
tile_brown_png = pygame.image.load(os.path.join("images", "tile_brown.png"))
tile_white_png = pygame.image.load(os.path.join("images", "tile_white.png"))
tile_heart_png = pygame.image.load(os.path.join("images", "tile_heart.png"))
tile_yellow_png = pygame.image.load(os.path.join("images", "tile_yellow.png"))
tile_flag_png = pygame.image.load(os.path.join("images", "tile_flag.png"))
tile_diamond_png = pygame.image.load(os.path.join("images", "tile_diamond.png"))

COLOR_MAP = {
    "red": tile_red_png,
    "green": tile_green_png,
    "blue": tile_blue_png,
    "brown": tile_brown_png,
    "white": tile_white_png,
    "heart": tile_heart_png,
    "yellow": tile_yellow_png,
    "flag": tile_flag_png,
    "diamond": tile_diamond_png
}

num_zero_png = pygame.image.load(os.path.join("images", "num_zero.png"))
num_one_png = pygame.image.load(os.path.join("images", "num_one.png"))
num_two_png = pygame.image.load(os.path.join("images", "num_two.png"))
num_three_png = pygame.image.load(os.path.join("images", "num_three.png"))
num_four_png = pygame.image.load(os.path.join("images", "num_four.png"))
num_five_png = pygame.image.load(os.path.join("images", "num_five.png"))
num_six_png = pygame.image.load(os.path.join("images", "num_six.png"))
num_seven_png = pygame.image.load(os.path.join("images", "num_seven.png"))
num_eight_png = pygame.image.load(os.path.join("images", "num_eight.png"))
num_nine_png = pygame.image.load(os.path.join("images", "num_nine.png"))

NUMBER_LIST = [
    num_zero_png, num_one_png, num_two_png, num_three_png, num_four_png, num_five_png, num_six_png, num_seven_png,
    num_eight_png, num_nine_png,
]

# an error will occur if pygame.mixer is used and no sound source is active(headphones not plugged in/speakers disabled)
soundEnabled = True
try:
    pygame.mixer.init()
    toggle_sound = pygame.mixer.Sound(os.path.join("audio", 'toggle_001.ogg'))
    switch_sound = pygame.mixer.Sound(os.path.join("audio", 'switch_001.ogg'))
    error_sound = pygame.mixer.Sound(os.path.join("audio", 'error_002.ogg'))
    switch_random_sound = pygame.mixer.Sound(os.path.join("audio", 'select_003.ogg'))
    puzzle_random_sound = pygame.mixer.Sound(os.path.join("audio", 'confirmation_001.ogg'))

    toggle_sound.set_volume(0.5)
    switch_sound.set_volume(0.5)
    error_sound.set_volume(0.5)
    switch_random_sound.set_volume(0.5)
    puzzle_random_sound.set_volume(0.5)
except pygame.error:
    soundEnabled = False


class Entity:
    COOLDOWN = 30

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cooldown_counter = 0
        self.img = num_zero_png

    def draw(self, window):
        self.cooldown()
        window.blit(self.img, (self.x, self.y))

    def cooldown(self):
        if self.cooldown_counter >= self.COOLDOWN:
            self.cooldown_counter = 0
        elif self.cooldown_counter > 0:
            self.cooldown_counter += 1


class Player(Entity):
    COOLDOWN = 30

    def __init__(self, x, y):
        super().__init__(x, y)
        self.img = player_png
        self.mask = pygame.mask.from_surface(self.img)

    def collision(self, obj):
        return collide(self, obj)


class Switch(Entity):
    COOLDOWN = 120

    def __init__(self, x, y, number, tile):
        super().__init__(x, y)
        self.cooldown_counter = 1
        self.isSwitched = False
        self.img = switch_left_png
        self.number = number
        self.number_img = NUMBER_LIST[number]
        self.tile_str = tile
        self.tile = COLOR_MAP[tile]
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        self.cooldown()
        window.blit(self.img, (self.x, self.y))
        window.blit(self.tile, (self.x - 15, self.y - 15))
        window.blit(self.number_img, (self.x + 15, self.y - 15))

    # randomizer cooldown
    def random_cooldown(self):
        if self.cooldown_counter >= self.COOLDOWN:
            self.cooldown_counter = 0
        elif self.cooldown_counter > 0:
            self.cooldown_counter += 1

    # set up randomness and timers
    def randomize_number_tile(self):
        self.isSwitched = False
        self.img = switch_left_png
        self.cooldown_counter = 1

        if bool(random.getrandbits(1)):
            self.number = random.randint(1, 9)
            self.number_img = NUMBER_LIST[self.number]
        if bool(random.getrandbits(1)):
            self.tile_str = random.choice(list(COLOR_MAP))
            self.tile = COLOR_MAP[self.tile_str]

    def set_img(self):
        if self.isSwitched:
            self.img = switch_right_png
        else:
            self.img = switch_left_png

    def use_switch(self, player, puzzle):
        success = True
        if not self.isSwitched:
            for piece in puzzle:
                if not piece.isPieceSolved:
                    if self.tile_str == piece.tile_str or self.number == piece.number:
                        if soundEnabled:
                            pygame.mixer.Sound.play(switch_sound)
                        piece.isPieceSolved = True
                        piece.indicator = circle_green_png
                        self.isSwitched = True
                        self.img = switch_right_png
                        success = True
                        break
                    else:
                        success = False
                        if soundEnabled:
                            pygame.mixer.Sound.play(error_sound)
                        break
        if not success:
            for p in puzzle:
                p.isPieceSolved = False
                p.indicator = circle_red_png


# puzzle_answer is the solved puzzle and valid inputs to solve it
# each piece of it represents the allowed solution and whether or not the was a correct passed value
class Puzzle(Entity):
    COOLDOWN = 600

    def __init__(self, x, y, number, tile):
        super().__init__(x, y)
        self.cooldown_counter = 1
        self.number = number
        self.number_img = NUMBER_LIST[number]
        self.indicator = circle_red_png
        self.img = COLOR_MAP[tile]
        self.tile = tile
        self.tile_str = tile
        self.isPieceSolved = False

    def draw(self, window):
        self.cooldown()
        window.blit(self.img, (self.x - 15, self.y - 15))
        window.blit(self.number_img, (self.x + 15, self.y - 15))
        window.blit(self.indicator, (self.x, self.y + 15))

    def randomize_number_tile(self):
        if not self.isPieceSolved:
            self.cooldown_counter = 1

            # this can be changed along with the random cooldown timer to tweak probability of random change
            if bool(random.getrandbits(1)):
                self.number = random.randint(1, 9)
                self.number_img = NUMBER_LIST[self.number]
            if bool(random.getrandbits(1)):
                self.tile_str = random.choice(list(COLOR_MAP))
                self.tile = COLOR_MAP[self.tile_str]
                self.img = COLOR_MAP[self.tile_str]


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


FPS = 60
clock = pygame.time.Clock()


def main_game():
    run = True
    vel = 5

    won = False

    player = Player(400, 300)

    switches = [
        Switch(100, 200, 1, "red"),
        Switch(200, 200, 2, "blue"),
        Switch(300, 200, 3, "green"),
        Switch(400, 200, 4, "brown"),
        Switch(500, 200, 5, "diamond"),
        Switch(100, 400, 6, "heart"),
        Switch(200, 400, 7, "white"),
        Switch(300, 400, 8, "flag"),
        Switch(400, 400, 9, "yellow"),
    ]

    # set up puzzle
    puzzle_sequence = [
        Puzzle(50, 50, 1, "red"),
        Puzzle(110, 50, 2, "blue"),
        Puzzle(170, 50, 3, "green"),
        Puzzle(230, 50, 4, "brown"),
        Puzzle(290, 50, 5, "diamond"),
        Puzzle(350, 50, 6, "heart"),
        Puzzle(410, 50, 7, "white"),
        Puzzle(470, 50, 8, "flag"),
        Puzzle(530, 50, 9, "yellow"),
    ]

    def redraw_window():
        # replace with background later
        win.fill((0, 0, 0))

        player.draw(win)

        # separate loops for sound and loop optimization
        if switches[0].cooldown_counter == 0:
            if soundEnabled:
                pygame.mixer.Sound.play(switch_random_sound)
            for s1 in switches:
                s1.randomize_number_tile()

        for s1 in switches:
            s1.draw(win)

        # separate loops for sound and loop optimization
        # sound will probably break on the last piece, but it should be okay as the game will be over.
        if puzzle_sequence[len(puzzle_sequence)-1].cooldown_counter == 0:
            if soundEnabled:
                pygame.mixer.Sound.play(puzzle_random_sound)
            for p1 in puzzle_sequence:
                p1.randomize_number_tile()

        for piece in puzzle_sequence:
            piece.draw(win)

    while run:

        clock.tick(FPS)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()
                sys.exit()
                # pygame.quit()

        keys = pygame.key.get_pressed()

        # quit game or later escape menu
        if keys[pygame.K_ESCAPE]:
            run = False
            pygame.display.quit()
            pygame.quit()
            sys.exit()
        # left, right, up down
        if keys[pygame.K_a] and player.x > vel:
            player.x -= vel
        if keys[pygame.K_d] and player.x < 800:
            player.x += vel
        if keys[pygame.K_w] and player.y > 150:
            player.y -= vel
        if keys[pygame.K_s] and player.y < 600:
            player.y += vel
        if keys[pygame.K_SPACE]:
            for switch in switches:
                if player.collision(switch) and player.cooldown_counter == 0:
                    player.cooldown_counter = 1
                    if soundEnabled:
                        pygame.mixer.Sound.play(toggle_sound)
                    switch.use_switch(player, puzzle_sequence)

        pygame.display.update()

        for p in puzzle_sequence:
            won = p.isPieceSolved

        if won:
            run = False
            victory()


def intro():
    run_intro = True
    win.blit(intro_png, (0, 0))
    pygame.display.update()

    while run_intro:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_intro = False
                pygame.display.quit()
                pygame.quit()
                sys.exit()
                # pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                main_game()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            main_game()
        if keys[pygame.K_ESCAPE]:
            run_intro = False
            pygame.display.quit()
            pygame.quit()
            sys.exit()


def victory():
    run_victory = True
    win.blit(victory_png, (0, 0))
    pygame.display.update()

    while run_victory:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_victory = False
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                main_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main_game()
                if event.key == pygame.K_ESCAPE:
                    run_victory = False
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()


intro()
pygame.display.quit()
pygame.quit()
sys.exit()

"""
Extra todos:
- 
-  adjust probability with randrange for numbers and symbols. then you can shorten the cycle / cooldown time
    numbers should change less often as symbols are easier to deal with and 
    players will more than likely use symbols instead because it's easier.
- Add a single timer for the puzzle and switch cooldowns. remove the timer from each piece. 
- make a temporary set that the random changes pull from for unique set of changes, rather than having duplicate values
- possible to create a 'puzzle' class that has both the puzzle and switches in there, but it may complicate things.
# potentially can make it so left and right changes the properties so the player has some ability to manipulate them
reset field: switches only reset random counter if the player is in that field. forcing the player to move away from
    switches instead of camping them

# would be interesting to add mazes and enemies
#can add levels and maps later 
"""

