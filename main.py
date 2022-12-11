import pyxel

SCREEN_WIDTH = 320
SCREEN_HEIGHT = 180
CAPTION = 'Blackjack'
SCALE = 3

LOW_IMAGE = 'cards_low.png'
HIGH_IMAGE = 'cards_high.png'
# Card images adapted from those posted by reddit user BrontosaurusJewsus

CARD_WIDTH = 32
CARD_HEIGHT = 48


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title=CAPTION, display_scale=SCALE)
        # INITIALIZATION GOES HERE
        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pass


if __name__ == '__main__':
    App()
