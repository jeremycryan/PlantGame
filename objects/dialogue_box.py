import pygame
import string

import constants as c
import copy
from objects.dialogue import Dialogue


class DialogueBox:

    def __init__(self, scene):

        self.scene = scene
        self.player_mode = False
        self.current_selection = 1

        self.backdrop = pygame.Surface((c.BOX_WIDTH, c.BOX_HEIGHT))
        self.backdrop.fill(c.BOX_COLOR)
        self.backdrop.set_alpha(c.BOX_ALPHA)

        self.text_queue = []

        self.hidden = False
        self.frame_age = 0  # Time since the last text frame has been displayed
        self.font = pygame.font.SysFont("monospace", c.BOX_FONT_SIZE, bold=True)
        self.character_dict = {}
        self.set_dialogue(Dialogue("emilia_example", "Emilia"))
        for item in string.printable:
            self.character_dict[item] = self.font.render(item, 1, c.WHITE)

    def hide(self):
        self.hidden = True

    def show(self):
        self.hidden = False

    def draw(self):
        """ Draws the dialogue box on the screen. """

        if self.hidden:
            return

        x = c.BOX_MARGIN
        y = c.WINDOW_HEIGHT - c.BOX_HEIGHT - c.BOX_MARGIN
        self.scene.game.screen.blit(self.backdrop, (x, y))

        if not self.text_queue:
            return

        # Move cursor to draw characters
        cx, cy = x + c.BOX_PADDING, y + c.BOX_PADDING
        selector_x, selector_y = cx - self.character_dict[">"].get_width(), cy
        line_spacing = int(c.BOX_FONT_SIZE * c.BOX_FONT_SPACING)
        string_to_print = self.text_queue[0]
        if self.player_mode:
            string_to_print = "\n".join(self.text_queue)
        chars_to_display = int(self.frame_age * c.BOX_CHARACTER_RATE)
        chars_displayed = 0
        for word in string_to_print.split(" "):
            word_width = sum([self.character_dict[char].get_width() for char in word])
            for char in word:
                if cx + word_width > c.WINDOW_WIDTH - c.BOX_PADDING - c.BOX_MARGIN or char is "\n":
                    cx = x + c.BOX_PADDING
                    cy += line_spacing
                if char is not "\n":
                    char_surf = self.character_dict[char]
                    self.scene.game.screen.blit(char_surf, (cx, cy))
                    cx += char_surf.get_width()
                    word_width -= char_surf.get_width()
                chars_displayed += 1
                if chars_displayed >= chars_to_display:
                    break
            if chars_displayed >= chars_to_display:
                break
            cx += self.character_dict[" "].get_width()

        selector_y += int((self.current_selection - 1) * c.BOX_FONT_SPACING * c.BOX_FONT_SIZE)
        if self.player_mode:
            self.scene.game.screen.blit(self.character_dict[">"], (selector_x, selector_y))

    def update(self, dt, events):
        if self.hidden:
            return

        self.frame_age += dt

        for event in events:
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_DOWN) and (self.current_selection < len(self.text_queue)):
                    self.current_selection += 1
                if (event.key == pygame.K_UP) and (self.current_selection > 1):
                    self.current_selection -= 1
                if event.key == pygame.K_SPACE:
                    if self.text_is_done_drawing():
                        print(self.player_mode)
                        self.next_frame()

    def text_is_done_drawing(self):
        if not self.text_queue:
            return True
        chars_displayed = int(self.frame_age * c.BOX_CHARACTER_RATE)
        return chars_displayed > len(self.text_queue[0])

    def set_speech_block(self, speech_block):
        self.text_queue = copy.copy(speech_block.speechText)
        if speech_block.speechType == 'NPC':
            self.player_mode = False
        else:
            self.player_mode = True

    def set_dialogue(self, newDialogue):
        self.dialogue = newDialogue
        self.dialogue_iter = self.dialogue.do_dialogue()
        self.set_speech_block(self.dialogue_iter.__next__())

    def next_frame(self):
        """ Goes to the next frame of speech. """
        self.frame_age = 0
        if self.text_queue:
            if self.player_mode:
                self.text_queue = []
            else:
                self.text_queue.pop(0)
            if not self.text_queue:
                if self.player_mode:
                    self.dialogue.set_next_block(self.current_selection)
                else:
                    self.dialogue.set_next_block(1)
                print("test")
                try:
                    speech_block = self.dialogue_iter.__next__()
                    self.set_speech_block(speech_block)
                except StopIteration:
                    self.hide()
