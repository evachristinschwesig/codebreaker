from menu import Menu
from button import Button
from radio_button import RadioButton
from rules import Rules
from gameplay import Gameplay
from gameplay import Difficulty


class MainMenu(Menu):
    # Default difficulty: normal
    difficulty = Difficulty.NORMAL

    def __init__(self, manager, mixer):
        Menu.__init__(self, manager)

        # Load sound
        self.mixer = mixer
        self.mixer.music.set_volume(0.025)
        self.mixer.music.load('sound/Menu.ogg')
        self.mixer.music.play(loops=-1)

        # Header
        self.head = 'MAIN MENU'
        self.head_img = self.header_font.render(self.head, True, self.txt_color)
        head_img_size = self.head_img.get_size()
        head_img_center = (head_img_size[0] / 2, head_img_size[1] / 2)
        head_img_x = self.rect_center[0] - head_img_center[0]
        head_img_y = self.y + 15
        self.head_img_pos = (head_img_x, head_img_y)

        # Subtitle
        self.sub = 'Please select a difficulty'
        self.sub_img = self.sub_font.render(self.sub, True, self.txt_color)
        sub_img_size = self.sub_img.get_size()
        sub_img_center = (sub_img_size[0] / 2, sub_img_size[1] / 2)
        sub_img_x = self.rect_center[0] - sub_img_center[0]
        sub_img_y = self.y + 50
        self.sub_img_pos = (sub_img_x, sub_img_y)

        # Radio Buttons
        self.easy_rad = RadioButton(self.x + 80, 175, 'Easy')
        self.normal_rad = RadioButton(self.x + 80, 225, 'Normal')
        self.normal_rad.selected = True
        self.normal_rad.fill_color = (0, 0, 0)
        self.hard_rad = RadioButton(self.x + 80, 275, 'Hard')

        # Buttons
        self.rules_btn = Button(self.x + 10, self.y + self.height - 50, self.header_font, 'Rules')
        self.start_btn = Button(self.x + self.width - 140, self.y + self.height - 50, self.header_font, 'Start')

        # Highlightable objects
        self.highlightable.append(self.rules_btn)
        self.highlightable.append(self.start_btn)
        self.highlightable.append(self.easy_rad)
        self.highlightable.append(self.normal_rad)
        self.highlightable.append(self.hard_rad)

        # Set radio group
        radio_group = [self.easy_rad, self.normal_rad, self.hard_rad]
        for btn in radio_group:
            btn.group = radio_group

        # On-clicked property
        self.rules_btn.on_clicked = self.on_rules_btn_clicked
        self.start_btn.on_clicked = self.on_start_btn_clicked

        # On-selected property
        self.easy_rad.on_selected = self.on_easy_selected
        self.normal_rad.on_selected = self.on_normal_selected
        self.hard_rad.on_selected = self.on_hard_selected

    def on_easy_selected(self):
        self.difficulty = Difficulty.EASY

    def on_normal_selected(self):
        self.difficulty = Difficulty.NORMAL

    def on_hard_selected(self):
        self.difficulty = Difficulty.HARD

    def on_rules_btn_clicked(self):
        self.manager.push(Rules(self.manager))

    def on_start_btn_clicked(self):
        self.manager.pop()
        self.manager.push(Gameplay(self.manager, self.difficulty, self.mixer))

    def draw(self, screen):
        Menu.draw(self, screen)
        screen.blit(self.head_img, self.head_img_pos)
        screen.blit(self.sub_img, self.sub_img_pos)

        for obj in self.highlightable:
            obj.draw(screen)

    def destroy(self):
        self.mixer.stop()
