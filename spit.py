import pygame
import pickle

class Label():
    def __init__(self,
                 x: int,
                 y: int,
                 value: str,
                 fg_color: pygame.Color,
                 font_size: int = 16,
                 font_string: str = "data/fonts/default_fira.ttf",
                 ):
        
        """ Draws static text to the screen
        
        Arguments:
        x: int - the horizontal position of the text field
        y: int - the vertical position of the text field
        value: str - the text that will be displayed in the label
        fg_color: pygame.Color - the color of the text
        font_size: int=16 - the size of the font on screen
        font_string: str="data/fonts/default_fira.ttf" - the path of the font used for the field, uses the FiraCode Mono Nerd Font by default
        """

        self.pos = pygame.math.Vector2(x, y)

        self.fg_color = fg_color

        self.font_size = font_size
        self.font_string = font_string

        self.text = value
        self.font = pygame.font.Font(self.font_string, self.font_size)
        self.rendered_text = self.font.render(self.text, True, (self.fg_color))

        self.display_surface = pygame.display.get_surface()

    def draw(self):
        self.display_surface.blit(self.rendered_text, self.pos)

class TextField():
    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 name: str,
                 fg_color: pygame.Color,
                 bg_color: pygame.Color,
                 hl_color: pygame.Color,
                 draw_type = "box",
                 font_size = 16,
                 alignment = "left",
                 path_prefix = "data/textfields/",
                 font_string = "data/fonts/default_fira.ttf",
                 value = ""
                 ):
        
        """ Simple text field (overflow allowed)
        
        Arguments:
        x: int - the horizontal position of the text field
        y: int - the vertical position of the text field
        width: int - the total width of the text field (text can overflow this)
        height: int - the total height of the text field (this class does not support multi-line text)
        name: str - the unique name of the text field, used for saving and loading the content
        fg_color: pygame.Color - the color of the text
        bg_color: pygame.Color - the default color of the bounding box, used for the draw_type
        hl_color: pygame.Color - the higlight color for when the field state is focused
        draw_type: str="box" - "box" "line" or "none", used for determining how much of the bounding box should be rendered
        font_size: int=16 - the size of the font on screen
        alignment: str="left" - "left" "center" the horizontal alignment of the text in the field
        path_prefix: str="data/textfields/" - the path that the field content will be saved to
        font_string: str="data/fonts/default_fira.ttf" - the path of the font used for the field, uses the FiraCode Mono Nerd Font by default 
        value: str="" - the value the field will load with by default
        """
        
        self.pos = pygame.math.Vector2(x, y)

        self.width = width
        self.height = height

        self.name = name
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.hl_color = hl_color
        self.draw_type = draw_type
        self.font_size = font_size
        self.alignment = alignment
        self.path_prefix = path_prefix
        self.font_string = font_string

        self.focused = False

        self.text = value
        self.font = pygame.font.Font(self.font_string, self.font_size)
        self.rendered_text = self.font.render(self.text, True, (self.fg_color))

        self.display_surface = pygame.display.get_surface()

    def draw(self):
        if self.focused:
            if self.draw_type == "box":
                pygame.draw.rect(self.display_surface, self.hl_color, (self.pos.x, self.pos.y, self.width, self.height), 1)
            elif self.draw_type == "line":
                pygame.draw.line(self.display_surface, self.hl_color, (self.pos.x, self.pos.y + self.height), (self.pos.x + self.width, self.pos.y + self.height))
            elif self.draw_type == "none":
                pass
        else:
            if self.draw_type == "box":
                pygame.draw.rect(self.display_surface, self.bg_color, (self.pos.x, self.pos.y, self.width, self.height), 1)
            elif self.draw_type == "line":
                pygame.draw.line(self.display_surface, self.bg_color, (self.pos.x, self.pos.y + self.height), (self.pos.x + self.width, self.pos.y + self.height))
            elif self.draw_type == "none":
                pass

        if self.alignment == "centered":
            self.display_surface.blit(self.rendered_text, (int(self.pos.x + (self.width / 2) - (self.rendered_text.get_width() / 2)), self.pos.y))
        elif self.alignment == "left":
            self.display_surface.blit(self.rendered_text, self.pos)

    def update(self, events):
        self.check_focused(events)

        self.rendered_text = self.font.render(self.text, True, self.fg_color)

        if self.focused:
            self.get_keyboard_input(events)

    def check_focused(self, events):
        pos = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.pos.x < pos[0] < self.pos.x + self.width:
                    if self.pos.y < pos[1] < self.pos.y + self.height:
                        self.focused = True
                    else:
                        self.focused = False
                else:
                    self.focused = False

    def get_keyboard_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.focused = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def save(self):
        pickle.dump(self.text, open(str(self.path_prefix + self.name + "_text.p"), "wb+"))

    def load(self):
        try:
            self.text = pickle.load(open(str(self.path_prefix + self.name + "_text.p"), "rb"))
        except:
            pass