from menu import Menu
from button import Button
from slot import Slot
import pygame as pg


class EndGame(Menu):
    def __init__(self, manager, text, difficulty, mixer, code):
        Menu.__init__(self, manager)
        self.difficulty = difficulty

        # Load sound
        self.mixer = mixer
        self.win_fx = pg.mixer.Sound('sound/Win.wav')
        self.win_fx.set_volume(0.025)

        self.lose_fx = pg.mixer.Sound('sound/GameOver.wav')
        self.lose_fx.set_volume(0.025)

        if text == 'YOU WIN':
            self.win_fx.play()
        elif text == 'GAME OVER':
            self.lose_fx.play()

        self.code = code

        # Header
        self.head = text
        self.head_img = self.header_font.render(self.head, True, self.txt_color)
        head_img_size = self.head_img.get_size()
        head_img_center = (head_img_size[0] / 2, head_img_size[1] / 2)
        head_img_x = self.rect_center[0] - head_img_center[0]
        head_img_y = self.y + 100
        self.head_img_pos = (head_img_x, head_img_y)

        self.sub_text = 'The correct code is:'
        self.sub_img = self.sub_font.render(self.sub_text, True, self.txt_color)
        sub_img_size = self.sub_img.get_size()
        sub_img_center = (sub_img_size[0] / 2, sub_img_size[1] / 2)
        sub_img_x = self.rect_center[0] - sub_img_center[0]
        sub_img_y = self.y + 150
        self.sub_img_pos = (sub_img_x, sub_img_y)

        # Create slots to display correct code
        self.slots = []
        i = 0
        for x in range(0, 4):
            slot = Slot(x, 5)
            slot.color = self.code[i]
            self.slots.append(slot)
            i += 1

        # Buttons
        self.replay_btn = Button(self.x + 10, self.y + self.height - 50, self.header_font, 'Replay')
        self.menu_btn = Button(self.x + self.width - 140, self.y + self.height - 50, self.header_font, 'Menu')

        # Highlightable objects
        self.highlightable.append(self.replay_btn)
        self.highlightable.append(self.menu_btn)

        # On-clicked property
        self.replay_btn.on_clicked = self.on_replay_btn_clicked
        self.menu_btn.on_clicked = self.on_menu_btn_clicked

    def on_replay_btn_clicked(self):
        # Starts new game with same difficulty
        from gameplay import Gameplay
        self.manager.pop()
        self.manager.push(Gameplay(self.manager, self.difficulty, self.mixer))

    def on_menu_btn_clicked(self):
        # Resets game, opens up main menu
        from main_menu import MainMenu
        self.manager.clear()
        self.manager.push(MainMenu(self.manager, self.mixer))

    def process_input(self, event):
        Menu.process_input(self, event)

    def draw(self, screen):
        Menu.draw(self, screen)
        screen.blit(self.head_img, self.head_img_pos)
        screen.blit(self.sub_img, self.sub_img_pos)

        for obj in self.highlightable:
            obj.draw(screen)

        for s in self.slots:
            s.draw(screen)

    def destroy(self):
        self.win_fx.stop()
        self.lose_fx.stop()
