import arcade

WALL_SCALING = 0.5
TRAP_SCALING = 0.2


class Fase1:

    def __init__(self) -> None:

        self.wall_list = None
        self.hero_list = None
        self.hero_sprite = None
        self.physics_engine = None
        self.init_area = None
        self.mobs_list = None
        self.corners = [(50, 550), (100, 500)]

    def setup(self):

        self.wall_list = arcade.SpriteList()
        self.hero_list = arcade.SpriteList()
        self.mobs_list = arcade.SpriteList()

        # setup the mobs

        # setup the hero
        self.hero_sprite = arcade.Sprite('sprites/hero.png')
        self.hero_sprite.center_x = 75
        self.hero_sprite.center_y = 100
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

        for x in range(self.corners[0][0], 500, 8):
            block = arcade.Sprite('sprites/tile_0031.png', WALL_SCALING)
            block.center_x = x
            block.center_y = 140
            self.wall_list.append(block)

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.hero_sprite, self.wall_list)

    def update(self):

        self.physics_engine.update()
        self.hero_sprite.center_x += self.hero_sprite.change_x
        self.hero_sprite.center_y += self.hero_sprite.change_y

    def draw(self):

        arcade.draw_rectangle_filled(
            75, 120, 40, 40, arcade.color.TEA_GREEN)
        self.wall_list.draw()
        self.hero_list.draw()
