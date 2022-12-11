import pyxel
from collections import namedtuple
from random import shuffle

SCREEN_WIDTH = 320
SCREEN_HEIGHT = 180
CAPTION = 'Blackjack'
SCALE = 3
FRAME_RATE = 40

Card = namedtuple('Card', ['suit', 'value'])
Vec2 = namedtuple('Vec2', ['x', 'y'])

CARD_WIDTH = 32
CARD_HEIGHT = 48
LOW_IMAGE = 'cards_low.png'
HIGH_IMAGE = 'cards_high.png'
# Card images adapted from those posted by reddit user BrontosaurusJewsus
LOW_BANK = 0
HIGH_BANK = 1

SHOE_LOC = Vec2(CARD_WIDTH // 2, CARD_WIDTH // 2)
DEALER_LOC = Vec2(SCREEN_WIDTH // 2 + CARD_WIDTH, CARD_HEIGHT // 2)
PLAYER_LOC = Vec2(SCREEN_WIDTH // 2 - (3 * CARD_WIDTH // 2), (3 * SCREEN_HEIGHT // 4) - (CARD_HEIGHT // 2))
SPLIT_LOC = Vec2(SCREEN_WIDTH // 2 + CARD_WIDTH // 4, PLAYER_LOC.y)
STACK_LOC = Vec2(4, SCREEN_HEIGHT - pyxel.FONT_HEIGHT - 4)
BET_TEXT_LOC = Vec2(8, STACK_LOC.y - 4 * (pyxel.FONT_HEIGHT + 1))
ACTIONS_TEXT_LOC = Vec2(SCREEN_WIDTH - (9 * pyxel.FONT_WIDTH) - 4)

STACK_DEFAULT = 500
MIN_BET = 10
SHOE_SIZE = 8

DEAL_SPEED = CARD_WIDTH // 3    # in pixels per frame
HAND_OFFSET = CARD_WIDTH // 3   # horizontal offset per card when drawing hand
SHOE_OFFSET = CARD_WIDTH // 4   # horizontal offset per face down card when drawing the shoe

class Hand(list):

    def total(self, ignore_first=False):
        total_ = 0
        ace = False
        if ignore_first:
            if len(self) > 1:
                for card_ in self[1:]:
                    if not ace and card_.value == 1:
                        ace = True
                    total_ += min(card_.value, 10)
        else:
            for card_ in self:
                if not ace and card_.value == 1:
                    ace = True
                total_ += min(card_.value, 10)
        if total_ <= 11 and ace:
            total_ += 10
        return total_

    def total_str(self, ignore_first=False):
        total = 0
        ace = False
        if ignore_first:
            if len(self) > 1:
                for card_ in self[1:]:
                    if not ace and card_.value == 1:
                        ace = True
                    total += min(card_.value, 10)
        else:
            for card_ in self:
                if not ace and card_.value == 1:
                    ace = True
                total += min(card_.value, 10)
        if total <= 11 and ace:
            return f'/{total + 10}'
        return str(total)


def create_decks(num):
    deck = []
    for _ in range(int(num)):
        for s in range(4):
            for v in range(1, 14):
                deck.append(Card(s, v))
    shuffle(deck)
    return deck


def draw_card(card_, x, y, face_down=False, card_back=0):
    if face_down:
        pyxel.blt(x, y, LOW_BANK, 0, card_back * CARD_HEIGHT, CARD_WIDTH, CARD_HEIGHT)
    elif card_.value <= 6:
        pyxel.blt(x, y, LOW_BANK, card_.value * CARD_WIDTH, card_.suit * CARD_HEIGHT, CARD_WIDTH, CARD_HEIGHT)
    else:
        pyxel.blt(x, y, HIGH_BANK, (card_.value - 7) * CARD_WIDTH, card_.suit * CARD_HEIGHT, CARD_WIDTH, CARD_HEIGHT)


def draw_hand(hand_, x, y, ignore_first=False):
    # draw cards
    for i, card_ in enumerate(hand_):
        if ignore_first and i == 0:
            draw_card(card_, x + i * HAND_OFFSET, y, face_down=True)
        else:
            draw_card(card_, x + i * HAND_OFFSET, y)
    # draw total text
    pyxel.text(x + CARD_WIDTH // 2, y - pyxel.FONT_HEIGHT - 3, hand_.total_str(ignore_first=ignore_first), pyxel.COLOR_YELLOW)


def draw_shoe(shoe):
    if shoe:
        for i in range(min(len(shoe) // 50, 1)):
            draw_card(Card(0, 1), SHOE_LOC.x + i * SHOE_OFFSET, SHOE_LOC.y, face_down=True)


class App:
    def __init__(self):
        # TODO -- load settings and stack size from file?
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title=CAPTION, fps=FRAME_RATE, display_scale=SCALE)
        pyxel.image(LOW_BANK).load(0, 0, LOW_IMAGE)
        pyxel.image(HIGH_BANK).load(0, 0, HIGH_IMAGE)
        self.state = 'intro'    # states are: intro, bet, deal, player turn, dealer turn, payout
        self.bg_color = pyxel.COLOR_GREEN
        self.stack = STACK_DEFAULT
        self.player_hand = Hand()
        self.split_hand = Hand()
        self.dealer_hand = Hand()
        self.shoe = create_decks(SHOE_SIZE)
        pyxel.run(self.update, self.draw)

    def update(self):
        pyxel.mouse(True)
        if self.state == 'intro':
            # stay in intro until Enter (either one) is hit
            if pyxel.btn(pyxel.KEY_RETURN) or pyxel.btn(pyxel.KEY_KP_ENTER):
                self.state = 'bet'
        elif self.state == 'bet':
            pass
        elif self.state == 'deal':
            pass
        elif self.state == 'player':
            pass
        elif self.state == 'dealer':
            pass
        elif self.state == 'payout':
            pass

    def draw(self):
        pyxel.cls(self.bg_color)
        if self.state == 'intro':
            pass
        elif self.state == 'bet':
            draw_shoe(self.shoe)
            # TODO -- draw bet text
        elif self.state == 'deal':
            draw_shoe(self.shoe)
            draw_hand(self.player_hand, PLAYER_LOC.x, PLAYER_LOC.y)
            draw_hand(self.dealer_hand, DEALER_LOC.x, DEALER_LOC.y, ignore_first=True)
        elif self.state == 'player':
            draw_shoe(self.shoe)
            draw_hand(self.player_hand, PLAYER_LOC.x, PLAYER_LOC.y)
            draw_hand(self.dealer_hand, DEALER_LOC.x, DEALER_LOC.y, ignore_first=True)
            # TODO -- actions text
        elif self.state == 'dealer':
            draw_shoe(self.shoe)
            draw_hand(self.player_hand, PLAYER_LOC.x, PLAYER_LOC.y)
            draw_hand(self.dealer_hand, DEALER_LOC.x, DEALER_LOC.y)
        elif self.state == 'payout':
            draw_shoe(self.shoe)
            draw_hand(self.player_hand, PLAYER_LOC.x, PLAYER_LOC.y)
            draw_hand(self.dealer_hand, DEALER_LOC.x, DEALER_LOC.y)

    def deal_card(self):
        # TODO -- find distance between shoe location and destination
        # TODO -- find number of frames the animation lasts (distance / speed)
        # TODO -- loop that number of times, first calling self.draw(), then drawing the card (back) being dealt
        # TODO -- and last, actually take the card object from the shoe list and add it to the destination hand list
        pass


if __name__ == '__main__':
    App()
