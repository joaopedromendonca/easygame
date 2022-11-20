import arcade

SPRITE_SCALING = 0.5


class Fase1:

    def __init__(self) -> None:

        self.wall_list = None
        self.hero_list = None
        self.hero_sprite = None
        self.physics_engine = None

    def setup(self):

        self.corners = [(50, 550), (100, 500)]
        self.wall_list = arcade.SpriteList()
        self.hero_list = arcade.SpriteList()

        self.hero_sprite = arcade.Sprite('sprites/creature-1.png')
        self.hero_sprite.center_x = 100
        self.hero_sprite.center_y = 200
        self.hero_list.append(self.hero_sprite)

        for x in range(self.corners[0][0], self.corners[0][1], 8):
            block = arcade.Sprite('sprites/tile_0031.png', SPRITE_SCALING)
            block.center_x = x
            block.center_y = 100
            self.wall_list.append(block)

        for x in range(self.corners[0][0], self.corners[0][1], 8):
            block = arcade.Sprite('sprites/tile_0031.png', SPRITE_SCALING)
            block.center_x = x
            block.center_y = 500
            self.wall_list.append(block)

        for y in range(self.corners[1][0], self.corners[1][1], 8):
            block = arcade.Sprite('sprites/tile_0031.png', SPRITE_SCALING)
            block.center_x = 50
            block.center_y = y
            self.wall_list.append(block)

        for y in range(self.corners[1][0], self.corners[1][1], 8):
            block = arcade.Sprite('sprites/tile_0031.png', SPRITE_SCALING)
            block.center_x = 546
            block.center_y = y
            self.wall_list.append(block)

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.hero_sprite, self.wall_list)

    def update(self):

        self.physics_engine.update()
        self.hero_sprite.center_x += self.hero_sprite.change_x
        self.hero_sprite.center_y += self.hero_sprite.change_y

    def draw(self):

        self.wall_list.draw()
        self.hero_list.draw()

        # arcade.draw_rectangle_outline(center_x=300, center_y=300, width=500,
        #                               height=300, color=arcade.color.BLUE_SAPPHIRE, border_width=2)
