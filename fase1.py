from time import sleep
import arcade
from arcade.experimental.lights import Light, LightLayer
WALL_SCALING = 0.5
TRAP_SCALING = 0.2
SAFE_AREA_LEN = 40
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
AMBIENT_COLOR = (10, 10, 10)


class Mob():

    def __init__(self, begin_x, begin_y, end_x, end_y, speed, dir) -> None:

        self.mob_sprite = arcade.Sprite('sprites/mob.png')
        self.mob_begin_x = begin_x
        self.mob_begin_y = begin_y
        self.mob_end_x = end_x
        self.mob_end_y = end_y
        self.mob_sprite.center_x = begin_x
        self.mob_sprite.center_y = begin_y
        self.mob_speed = speed
        self.dir = dir

    def update(self):

        if self.dir == 'h':
            if self.mob_sprite.center_x < self.mob_begin_x:
                self.mob_speed *= -1
            elif self.mob_sprite.center_x > self.mob_end_x:
                self.mob_speed *= -1
            self.mob_sprite.center_x += self.mob_speed

        elif self.dir == 'v':
            if self.mob_sprite.center_y < self.mob_begin_y:
                self.mob_speed *= -1
            elif self.mob_sprite.center_y > self.mob_end_y:
                self.mob_speed *= -1
            self.mob_sprite.center_y += self.mob_speed
        self.mob_sprite.update()

    def draw(self):
        self.mob_sprite.draw()


def wall_box(x_0, y_0, width, height):

    wall = []
    for x in range(x_0, x_0+width, 8):
        block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
        block.center_x = x
        block.center_y = y_0
        wall.append(block)
        block2 = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
        block2.center_x = x
        block2.center_y = y_0 + height
        wall.append(block2)

    for y in range(y_0, y_0+height+8, 8):
        block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
        block.center_x = x_0
        block.center_y = y
        wall.append(block)
        block2 = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
        block2.center_x = x_0 + width
        block2.center_y = y
        wall.append(block2)

    return wall


class Fase1:

    def __init__(self) -> None:

        self.wall_list = None
        self.hero_list = None
        self.hero_sprite = None
        self.physics_engine = None
        self.init_area = None
        self.mobs_list = None
        self.mobs = []
        self.corners = [(50, 550), (100, 500)]
        self.hero_alive = None

        # light
        self.light_layer = None
        self.player_light = None

    def setup(self):

        self.background_sprite_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.hero_list = arcade.SpriteList()
        self.mobs_list = arcade.SpriteList()
        self.death_count = 0

        # setup the mobs
        mob = Mob(245, 120, 475, 120, 1, 'h')
        mob2 = Mob(160, 480, 475, 420, 1, 'h')
        mob3 = Mob(164, 180, 164, 448, 1, 'v')
        self.mobs.append(mob)
        self.mobs.append(mob2)
        self.mobs.append(mob3)
        self.mobs_list.append(mob.mob_sprite)
        self.mobs_list.append(mob2.mob_sprite)
        self.mobs_list.append(mob3.mob_sprite)

        # setup the hero
        self.hero_sprite = arcade.Sprite('sprites/hero.png')
        self.hero_alive = True
        self.hero_sprite.center_x = 75
        self.hero_sprite.center_y = 110
        self.hero_list.append(self.hero_sprite)

        # setup lights
        for x in range(54, SCREEN_WIDTH-54, 8):
            for y in range(104, SCREEN_HEIGHT-100, 8):
                sprite = arcade.Sprite(
                    "sprites/tile_0000.png")
                sprite.center_x = x
                sprite.center_y = y
                # sprite.position = x, y
                self.background_sprite_list.append(sprite)

        self.light_layer = LightLayer(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.light_layer.set_background_color(arcade.color.BLACK)
        self.light_radius_player = 30

        # player light
        radius = 50
        mode = 'soft'
        color = arcade.csscolor.WHITE
        self.player_light = Light(0, 0, radius, color, mode)
        self.light_layer.add(self.player_light)

        # walls
        for x in range(self.corners[0][0], self.corners[0][1], 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = x
            block.center_y = 100
            self.wall_list.append(block)

        for x in range(self.corners[0][0], self.corners[0][1], 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = x
            block.center_y = 500
            self.wall_list.append(block)

        for y in range(self.corners[1][0], self.corners[1][1], 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = 50
            block.center_y = y
            self.wall_list.append(block)

        for y in range(self.corners[1][0], self.corners[1][1], 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = 546
            block.center_y = y
            self.wall_list.append(block)

        # primeiro bloco esquerda
        for x in range(self.corners[0][0], 135, 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = x
            block.center_y = 140
            self.wall_list.append(block)

        for y in range(140, 300, 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = 138
            block.center_y = y
            self.wall_list.append(block)

        # safe area
        for x in range(106, 144, 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = x
            block.center_y = 300
            self.wall_list.append(block)
            block2 = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block2.center_x = x
            block2.center_y = 340
            self.wall_list.append(block2)

        for y in range(300, 340, 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = 106
            block.center_y = y
            self.wall_list.append(block)

        for y in range(340, 460, 8):
            block2 = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block2.center_x = 138
            block2.center_y = y
            self.wall_list.append(block2)

        for x in range(106, 144, 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = x
            block.center_y = 460
            self.wall_list.append(block)

        for y in range(460, 500, 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = 106
            block.center_y = y
            self.wall_list.append(block)

        self.wall_list.extend(wall_box(190, 140, 104, 320))
        self.wall_list.extend(wall_box(350, 140, 88, 80))
        self.wall_list.extend(wall_box(350, 260, 88, 200))

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.hero_sprite, self.wall_list)

    def set_player_light(self):

        mode = 'soft'
        color = arcade.csscolor.WHITE
        self.player_light = Light(
            self.hero_sprite.center_x, self.hero_sprite.center_y, self.light_radius_player, color, mode)
        self.light_layer.add(self.player_light)

    def update(self):

        if self.hero_alive == False:
            self.hero_sprite.center_x = 75
            self.hero_sprite.center_y = 110
            self.hero_alive = True

        self.physics_engine.update()
        self.mobs_list.update()

        self.player_light.position = self.hero_sprite.position
        self.hero_sprite.position += (self.hero_sprite.change_x,
                                      self.hero_sprite.change_y)

        if arcade.check_for_collision_with_list(
                self.hero_sprite, self.mobs_list) != []:
            self.hero_alive = False
            self.death_count += 1
            sleep(0.3)

    def safe_area(self, center_x, center_y, radius=20):
        mode = 'soft'
        color = arcade.csscolor.WHITE
        light = Light(center_x, center_y, radius, color, mode)
        self.light_layer.add(light)

    def draw(self):

        with self.light_layer:
            self.background_sprite_list.draw()
            self.hero_list.draw()
            self.mobs_list.draw()

        self.light_layer.draw(ambient_color=AMBIENT_COLOR)

        pos = (self.hero_sprite.center_x, self.hero_sprite.center_y)
        arcade.draw_text(pos, start_x=50, start_y=50,
                         color=arcade.color.ALABAMA_CRIMSON)
        death_count = f'DEATHS: {self.death_count}'
        arcade.draw_text(death_count, start_x=200, start_y=50,
                         color=arcade.color.ALABAMA_CRIMSON)

        # self.safe_area(75, 120)
        self.safe_area(122, 320)
        self.safe_area(122, 480)

        self.wall_list.draw()
        # self.hero_list.draw()
        for mob in self.mobs:
            mob.update()
