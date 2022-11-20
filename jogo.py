import arcade
from fase1 import Fase1
from hero import Hero

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
MOVE_KEYS = [arcade.key.LEFT, arcade.key.RIGHT, arcade.key.UP, arcade.key.DOWN]


class GameWindow(arcade.Window):

    def __init__(self, width, height, title) -> None:

        super().__init__(width, height, title)

        self.hero_list = None
        self.wall_list = None

        self.hero_sprite = None

        self.hero = Hero(x_pos=300, y_pos=50)
        self.fase1 = Fase1()

    def setup(self):

        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.fase1.setup()

    def on_draw(self) -> None:

        arcade.start_render()
        self.fase1.draw()

    def update(self, delta_time: float):
        self.fase1.update()

    def on_key_press(self, key: int, modifiers: int):

        if key == arcade.key.UP:
            self.fase1.hero_sprite.change_y = self.hero.vel
        elif key == arcade.key.DOWN:
            self.fase1.hero_sprite.change_y = -self.hero.vel
        elif key == arcade.key.LEFT:
            self.fase1.hero_sprite.change_x = -self.hero.vel
        elif key == arcade.key.RIGHT:
            self.fase1.hero_sprite.change_x = self.hero.vel

    def on_key_release(self, key: int, modifiers: int):

        if key == arcade.key.UP:
            self.fase1.hero_sprite.change_y = 0
        elif key == arcade.key.DOWN:
            self.fase1.hero_sprite.change_y = 0
        elif key == arcade.key.LEFT:
            self.fase1.hero_sprite.change_x = 0
        elif key == arcade.key.RIGHT:
            self.fase1.hero_sprite.change_x = 0


def main():

    game_window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, "hero boi")
    game_window.setup()
    game_window.run()


if __name__ == '__main__':
    main()
