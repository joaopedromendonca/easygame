from time import sleep, time
import arcade
from arcade.experimental.lights import Light, LightLayer
WALL_SCALING = 0.5
TRAP_SCALING = 0.2
SAFE_AREA_LEN = 40
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
AMBIENT_COLOR = (240, 240, 240)


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

        elif self.dir == 'd':
            if self.mob_sprite.center_y < self.mob_begin_y:
                self.mob_speed *= -1
            elif self.mob_sprite.center_y > self.mob_end_y:
                self.mob_speed *= -1
            self.mob_sprite.center_y += self.mob_speed
            self.mob_sprite.center_x += self.mob_speed

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
        self.hero_alive = None
        self.torch_list = None
        # light
        self.light_layer = None
        self.player_light = None
        self.light_fade = 0

    def setup(self):

        self.background_sprite_list = arcade.SpriteList(
            use_spatial_hash=True)
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.hero_list = arcade.SpriteList()
        self.mobs_list = arcade.SpriteList()
        self.torch_list = arcade.SpriteList(use_spatial_hash=True)
        self.keys_list = arcade.SpriteList(use_spatial_hash=True)
        self.keys_found = 0
        self.death_count = 0
        self.last_time = 0
        # setup the mobs
        mob = Mob(245, 120, 475, 120, 1, 'h')
        mob2 = Mob(200, 480, 475, 420, 1, 'h')
        mob3 = Mob(214, 160, 214, 448, 1, 'v')
        mob4 = Mob(270, 200, 440, 200, 1, 'h')
        mob5 = Mob(340, 350, 450, 350, 1, 'h')
        mob6 = Mob(340, 400, 480, 400, 1, 'h')
        mob7 = Mob(340, 240, 310, 310, 1, 'd')
        mob8 = Mob(440, 240, 350, 310, 1, 'v')
        mob9 = Mob(140, 580, 320, 580, 0.8, 'h')
        mob9.mob_sprite.scale = 3
        mob10 = Mob(120, 626, 220, 626, 2.5, 'h')
        mob11 = Mob(230, 626, 340, 626, 2.5, 'h')
        mob12 = Mob()
        self.mobs.append(mob)
        self.mobs.append(mob2)
        self.mobs.append(mob3)
        self.mobs.append(mob4)
        self.mobs.append(mob5)
        self.mobs.append(mob6)
        self.mobs.append(mob7)
        self.mobs.append(mob8)
        self.mobs.append(mob9)
        self.mobs.append(mob10)
        self.mobs.append(mob11)
        self.mobs_list.append(mob.mob_sprite)
        self.mobs_list.append(mob2.mob_sprite)
        self.mobs_list.append(mob3.mob_sprite)
        self.mobs_list.append(mob4.mob_sprite)
        self.mobs_list.append(mob5.mob_sprite)
        self.mobs_list.append(mob6.mob_sprite)
        self.mobs_list.append(mob7.mob_sprite)
        self.mobs_list.append(mob8.mob_sprite)
        self.mobs_list.append(mob9.mob_sprite)
        self.mobs_list.append(mob10.mob_sprite)
        self.mobs_list.append(mob11.mob_sprite)

        # setup the hero
        self.hero_sprite = arcade.Sprite('sprites/hero.png')
        self.hero_alive = True
        self.hero_sprite.center_x = 100
        self.hero_sprite.center_y = 200
        self.hero_list.append(self.hero_sprite)

        key1 = arcade.Sprite('sprites/key.png', 0.3,
                             center_x=150, center_y=470)
        self.keys_list.append(key1)

        # key = arcade.Sprite('sprites/key.png', 1, )

        # setup lights
        for x in range(54, SCREEN_WIDTH-54, 8):
            for y in range(104, SCREEN_HEIGHT-50, 8):
                sprite = arcade.Sprite(
                    "sprites/tile_0000.png")
                sprite.center_x = x
                sprite.center_y = y
                self.background_sprite_list.append(sprite)

        self.light_layer = LightLayer(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.light_layer.set_background_color(arcade.color.BLACK)
        self.light_radius_player = 50

        # setup gate
        self.gate = arcade.Sprite(
            'sprites/door.png', 0.5, center_x=280, center_y=408)

        # setup torch
        torch = arcade.Sprite('sprites/torch.png', 0.1,
                              center_x=55, center_y=120)
        self.torch_list.append(torch)
        mode = 'soft'
        color = arcade.csscolor.LIGHT_YELLOW
        light = Light(55, 110, 10, color, mode)
        self.light_layer.add(light)

        torch = arcade.Sprite('sprites/torch.png', 0.1,
                              center_x=160, center_y=320)
        self.torch_list.append(torch)
        mode = 'soft'
        color = arcade.csscolor.LIGHT_YELLOW
        light = Light(160, 310, 10, color, mode)
        self.light_layer.add(light)

        torch = arcade.Sprite('sprites/torch.png', 0.1,
                              center_x=370, center_y=160)
        self.torch_list.append(torch)
        mode = 'soft'
        color = arcade.csscolor.LIGHT_YELLOW
        light = Light(370, 150, 10, color, mode)
        self.light_layer.add(light)

        torch = arcade.Sprite('sprites/torch.png', 0.1,
                              center_x=340, center_y=436)
        self.torch_list.append(torch)
        mode = 'soft'
        color = arcade.csscolor.LIGHT_YELLOW
        light = Light(340, 436, 10, color, mode)
        self.light_layer.add(light)

        torch = arcade.Sprite('sprites/torch.png', 0.1,
                              center_x=480, center_y=340)
        self.torch_list.append(torch)
        mode = 'soft'
        color = arcade.csscolor.LIGHT_YELLOW
        light = Light(480, 340, 10, color, mode)
        self.light_layer.add(light)

        torch = arcade.Sprite('sprites/torch.png', 0.1,
                              center_x=130, center_y=516)
        self.torch_list.append(torch)
        mode = 'soft'
        color = arcade.csscolor.LIGHT_YELLOW
        light = Light(130, 516, 10, color, mode)
        self.light_layer.add(light)

        # player light
        mode = 'soft'
        color = arcade.csscolor.WHITE
        self.player_light = Light(0, 0, self.light_radius_player, color, mode)
        self.light_layer.add(self.player_light)

        # walls
        for x in range(50, SCREEN_WIDTH-50, 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = x
            block.center_y = 100
            self.wall_list.append(block)

        for x in range(50, SCREEN_WIDTH-50, 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = x
            block.center_y = SCREEN_HEIGHT-52
            self.wall_list.append(block)

        for y in range(100, SCREEN_HEIGHT-50, 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = 50
            block.center_y = y
            self.wall_list.append(block)

        for y in range(100, SCREEN_HEIGHT-50, 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = SCREEN_WIDTH-54
            block.center_y = y
            self.wall_list.append(block)

        # primeiro bloco esquerda
        for x in range(50, 190, 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = x
            block.center_y = 140
            self.wall_list.append(block)

        for y in range(140, 300, 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = 186
            block.center_y = y
            self.wall_list.append(block)

        # safe area
        for x in range(154, 194, 8):
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
            block.center_x = 154
            block.center_y = y
            self.wall_list.append(block)

        # end safe area

        for y in range(340, 540, 8):
            block2 = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block2.center_x = 186
            block2.center_y = y
            self.wall_list.append(block2)

        for y in range(260, 610, 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = 106
            block.center_y = y
            self.wall_list.append(block)

        for x in range(240, 350, 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = x
            block.center_y = 140
            self.wall_list.append(block)

        # second safe area
        for y in range(140, 180, 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = 352
            block.center_y = y
            self.wall_list.append(block)
            block2 = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block2.center_x = 392
            block2.center_y = y
            self.wall_list.append(block2)

        for x in range(352, 400, 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = x
            block.center_y = 172
            self.wall_list.append(block)

        for y in range(148, 450, 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = 240
            block.center_y = y
            self.wall_list.append(block)

        for x in range(240, 328, 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = x
            block.center_y = 452
            self.wall_list.append(block)

        for y in range(224, 452, 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = 320
            block.center_y = y
            self.wall_list.append(block)

        for x in range(114, 370, 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = x
            block.center_y = 500
            self.wall_list.append(block)

        for x in range(400, 500, 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = x
            block.center_y = 140
            self.wall_list.append(block)

        for y in range(148, 460, 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = 496
            block.center_y = y
            self.wall_list.append(block)

        for x in range(360, 458, 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = x
            block.center_y = 452
            self.wall_list.append(block)

        for x in range(328, 358, 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = x
            block.center_y = 420
            self.wall_list.append(block)

        for y in range(420, 452, 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = 360
            block.center_y = y
            self.wall_list.append(block)

        for x in range(272, 464, 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = x
            block.center_y = 224
            self.wall_list.append(block)

        for y in range(184, 230, 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = 464
            block.center_y = y
            self.wall_list.append(block)

        for x in range(352, 500, 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = x
            block.center_y = 324
            self.wall_list.append(block)

        for x in range(50, 400, 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = x
            block.center_y = 644
            self.wall_list.append(block)

        for y in range(500, 640, 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = 394
            block.center_y = y
            self.wall_list.append(block)

        for y in range(500, 610, 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = 362
            block.center_y = y
            self.wall_list.append(block)

        # self.wall_list.extend(wall_box(290, 140, 104, 320))
        # self.wall_list.extend(wall_box(350, 140, 88, 80))
        # self.wall_list.extend(wall_box(350, 260, 88, 200))

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.hero_sprite, self.wall_list)

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

        _now_time = time()
        if _now_time - 2 > self.last_time:
            self.last_time = _now_time
            self.player_light.radius *= 0.95

        if arcade.check_for_collision_with_list(
                self.hero_sprite, self.mobs_list) != []:
            self.hero_alive = False
            self.death_count += 1
            sleep(0.3)

        if arcade.check_for_collision_with_list(
                self.hero_sprite, self.torch_list) != []:
            self.player_light.radius = self.light_radius_player

        if arcade.check_for_collision_with_list(self.hero_sprite, self.keys_list) != []:
            for k in self.keys_list:
                if arcade.check_for_collision(self.hero_sprite, k):
                    self.keys_list.remove(k)
                    self.keys_found += 1

    def draw(self):

        with self.light_layer:
            self.background_sprite_list.draw()
            self.mobs_list.draw()
            self.torch_list.draw()
            self.gate.draw()
            self.wall_list.draw()
            self.hero_list.draw()
            self.keys_list.draw()

        self.light_layer.draw(ambient_color=AMBIENT_COLOR)

        pos = (self.hero_sprite.center_x, self.hero_sprite.center_y)
        arcade.draw_text(pos, start_x=50, start_y=50,
                         color=arcade.color.ALABAMA_CRIMSON)
        death_count = f'DEATHS: {self.death_count}'
        arcade.draw_text(death_count, start_x=350, start_y=50,
                         color=arcade.color.ALABAMA_CRIMSON)
        rad = self.light_radius_player
        arcade.draw_text(rad, start_x=150, start_y=50,
                         color=arcade.color.ALABAMA_CRIMSON)

        keys_left = f'KEYS TO FIND: {3 - self.keys_found}'
        arcade.draw_text(keys_left, start_x=600, start_y=50,
                         color=arcade.color.ALABAMA_CRIMSON)

        for mob in self.mobs:
            mob.update()
