import arcade
from fase1 import Fase1

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
MOVE_KEYS = [arcade.key.LEFT, arcade.key.RIGHT, arcade.key.UP, arcade.key.DOWN]
SPEED = 1


class GameWindow(arcade.Window):

    def __init__(self, width, height, title) -> None:

        super().__init__(width, height, title)

        self.hero_list = None
        self.wall_list = None

        self.hero_sprite = None

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

        hero = self.fase1.hero_sprite
        if key == arcade.key.UP:
            hero.change_y = SPEED
        elif key == arcade.key.DOWN:
            hero.change_y = -SPEED
        elif key == arcade.key.LEFT:
            hero.change_x = -SPEED
        elif key == arcade.key.RIGHT:
            hero.change_x = SPEED

    def on_key_release(self, key: int, modifiers: int):
        '''
        bug no release de teclas da mesma direção sentido opostos
        '''

        if key == arcade.key.UP:
            self.fase1.hero_sprite.change_y = 0
        elif key == arcade.key.DOWN:
            self.fase1.hero_sprite.change_y = 0
        elif key == arcade.key.LEFT:
            self.fase1.hero_sprite.change_x = 0
        elif key == arcade.key.RIGHT:
            self.fase1.hero_sprite.change_x = 0
        elif self.fase1.win_game == True:
            if key == arcade.key.SPACE:
                self.fase1.setup()
        # cheat xd
        elif key == arcade.key.ESCAPE:
            self.fase1.win_game = True
        # lights up
        elif key == arcade.key.R:
            self.fase1.ambient_color = (20, 0, 0)
        elif key == arcade.key.B:
            self.fase1.ambient_color = (0, 0, 0)
        elif key == arcade.key.W:
            self.fase1.ambient_color = (240, 240, 240)


def main():

    game_window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, "hero boi")
    game_window.setup()
    game_window.run()


if __name__ == '__main__':
    main()
