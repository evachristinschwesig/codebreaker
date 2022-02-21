import pygame as pg
import random
from state import State
from pin import Pin
from slot import Slot
from button import Button
from turn import Turn


class Gameplay(State):
    # Dimensions
    width = 350
    height = 650
    # Colors
    bg = (210, 180, 140)
    grid = (50, 50, 50)
    empty_guess = (0, 0, 0)

    CODE_COLORS = ['red', 'yellow', 'green', 'blue', 'black', 'white']

    def __init__(self, manager):
        State.__init__(self, manager)
        self.num_rounds = 0
        self.code = None
        self.font = pg.font.SysFont('Calibri', 30)

        # Game objects
        self.pins = []
        self.slots = []
        self.buttons = []
        #self.highlightable = []
        self.turns = []

        # Create pins
        for y in range(0, 6):
            pin = Pin(y, self.CODE_COLORS[y])
            self.pins.append(pin)
            self.highlightable.append(pin)

        # Create slots
        for y in range(0, 12):
            for x in range(0, 4):
                slot = Slot(x, y)
                self.slots.append(slot)
                self.highlightable.append(slot)

        # Create buttons
        border = 20
        top = 610
        btn_width = 130

        self.submit_btn = Button(border, top, self.font, 'Submit')
        self.submit_btn.enabled = False
        self.buttons.append(self.submit_btn)
        self.highlightable.append(self.submit_btn)

        self.menu_btn = Button(self.width - border - btn_width, top, self.font, 'Menu')
        self.menu_btn.enabled = False
        self.buttons.append(self.menu_btn)
        self.highlightable.append(self.menu_btn)

        # On-clicked property
        self.submit_btn.on_clicked = self.on_submit_btn_clicked
        self.menu_btn.on_clicked = self.on_menu_btn_clicked

    def on_submit_btn_clicked(self):
        pass

    def on_menu_btn_clicked(self):
        pass

    def draw(self, screen):
        screen.fill(self.bg)

        # Draw grid lines
        for x in range(1, 12):
            pg.draw.line(screen, self.grid, (50, x * 50), (self.width, x * 50))

        pg.draw.line(screen, self.grid, (0, 600), (self.width, 600))
        pg.draw.line(screen, self.grid, (50, 0), (50, 600))
        pg.draw.line(screen, self.grid, (300, 0), (300, 600))

        # Draw pins
        for p in self.pins:
            p.draw(screen)

        # Draw slots
        if self.num_rounds == 8:
            for i in range(len(self.slots) - 16):
                self.slots[i].draw(screen)
        else:
            for s in self.slots:
                s.draw(screen)

        # Display buttons
        for b in self.buttons:
            b.draw(screen)

        # Display previous hints
        for t in self.turns:
            if 'black' in t.hint or 'white' in t.hint:
                t.show_hint(screen)

    def set_difficulty(self, difficulty):
        # Set difficulty
        if difficulty == 'easy' or difficulty == 'normal':
            self.num_rounds = 12
        elif difficulty == 'hard':
            self.num_rounds = 8

    def create_code(self, difficulty):
        # Generate code
        if difficulty == 'easy':
            self.code = (random.sample(self.CODE_COLORS, 4))
        elif difficulty == 'normal' or difficulty == 'hard':
            self.code = random.choices(self.CODE_COLORS, k=4)
        # print(self.code)

    def create_turns(self, difficulty):
        # Create turns
        curr_turn = 0
        if difficulty == 'easy' or difficulty == 'normal':
            for row in range(0, len(self.slots), 4):
                turn = Turn(self.slots[row:row + 4], curr_turn)
                self.turns.append(turn)
                curr_turn += 1
        elif difficulty == 'hard':
            for row in range(0, len(self.slots) - 16, 4):
                turn = Turn(self.slots[row:row + 4], curr_turn)
                self.turns.append(turn)
                curr_turn += 1

    def check_end(self, curr_hint, curr_turn):
        if len(curr_hint) == 4 and 'white' not in curr_hint and 'empty' not in curr_hint:
            #self.win_msg.draw(self.screen)
            self.highlightable = []
            return 'win'
        elif curr_turn == self.num_rounds - 1:
            #self.lose_msg.draw(self.screen)
            self.highlightable = []
            return 'loss'
        else:
            return None
