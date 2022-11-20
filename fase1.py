import arcade

WALL_SCALING = 0.5
TRAP_SCALING = 0.2


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

    def setup(self):

        self.wall_list = arcade.SpriteList()
        self.hero_list = arcade.SpriteList()
        self.mobs_list = arcade.SpriteList()

        # setup the mobs
        mob = Mob(275, 120, 475, 120, 1, 'h')
        mob2 = Mob(275, 420, 475, 420, 1, 'h')
        self.mobs.append(mob)
        self.mobs.append(mob2)
        self.mobs_list.append(mob.mob_sprite)
        self.mobs_list.append(mob2.mob_sprite)

        # setup the hero
        self.hero_sprite = arcade.Sprite('sprites/hero.png')
        self.hero_alive = True
        self.hero_sprite.center_x = 75
        self.hero_sprite.center_y = 110
        self.hero_list.append(self.hero_sprite)

        # traps
        # for y in range(140, 500, 20):
        #     for x in range(80, 400, 20):
        #         trap = arcade.Sprite('sprites/trap.png', TRAP_SCALING)
        #         trap.center_x = x
        #         trap.center_y = y
        #         self.traps_list.append(trap)

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

        for x in range(self.corners[0][0], 135, 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = x
            block.center_y = 140
            self.wall_list.append(block)

        for y in range(140, 350, 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = 138
            block.center_y = y
            self.wall_list.append(block)

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.hero_sprite, self.wall_list)

    def update(self):

        if self.hero_alive == False:
            self.hero_sprite.center_x = 75
            self.hero_sprite.center_y = 110
            self.hero_alive = True
        self.physics_engine.update()
        self.mobs_list.update()
        self.hero_sprite.center_x += self.hero_sprite.change_x
        self.hero_sprite.center_y += self.hero_sprite.change_y

        if arcade.check_for_collision_with_list(
                self.hero_sprite, self.mobs_list) != []:
            self.hero_alive = False

    def draw(self):
        pos = (self.hero_sprite.center_x, self.hero_sprite.center_y)
        arcade.draw_text(pos, start_x=50, start_y=50,
                         color=arcade.color.ALABAMA_CRIMSON)
        arcade.draw_rectangle_filled(
            75, 120, 40, 40, arcade.color.TEA_GREEN)
        self.wall_list.draw()
        self.hero_list.draw()
        self.mobs_list.draw()
        for mob in self.mobs:
            mob.update()
