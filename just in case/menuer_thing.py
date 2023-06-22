import pygame as pg
from pygame import Vector2, draw, Rect
import math


# Slider settings, all in terms of percent of box height

# How large the knob is
slider_knob_size = 0.2
# Where on the box the bar is displayed
slider_bar_height = 0.75
# How thick the bar is
slider_bar_thickness = 0.1
# How long the bar is, in terms of box width
slider_bar_length = 0.7
# How high text appears on the slider
slider_text_height = 0.6

# Text settings, all in terms of percent of box height

# How large text is (useful for different fonts)
text_box_size = 0.8
# Text focus bar blink rate, in terms of how many frames per cycle
text_focus_bar_rate = 30
text_focus_bar_tick = 0
# If text is centered or not
default_text_pos_x = "center"
default_text_pos_y = "center"
# How wide the text focus bar is
text_focus_bar_w = 0.06
# The font
default_font = "freesansbold.ttf"

#Toggle settings

#How big the knob is
toggle_knob_size = 0.7



# Draws a text box
def draw_text_box(
    screen: any,
    rect: pg.Rect,
    text: str,
    padding: int,
    text_color: str,
    background_color: str,
    font,
    include_box: bool = True,
    text_pos_x: str = "center",
    text_pos_y: str = "center",
):
    """
    Function to draw a text box onto window

    rect: The rect the box is
    text: the text in the box
    padding: How rounded the corners are
    text_size: size of text relative to box height
    text_color: The color of the text
    background_color: The color of the background
    text_pos_x: 'left', 'right', or 'center'
    text_pos_y: 'top', 'bottom', or 'center'
    """
    if include_box:
        pg.draw.rect(screen, background_color, rect, 0, padding)
    return draw_text(screen, rect, text, font, True, text_color, text_pos_x, text_pos_y)


# Text func
def draw_text(
    screen: any,
    _window: pg.Rect,
    text_str: str,
    font: pg.font.Font,
    aa: bool,
    fg: str,
    pos_x: str,
    pos_y: str,
) -> None:
    """
    Function to draw text on window

    text: text to draw on window (str)
    font: font to render the text with (pygame.font.Font)
    aa: use antialiasing (bool)
    fg: foreground color (str)
    bg: background color (str)
    _window: rect to draw text in
    pos_x: 'left', 'right', or 'center'
    pos_y: 'top', 'bottom', or 'center'
    """

    text = font.render(text_str, aa, fg)

    text_position = text.get_rect()
    text_position.topleft = _window.x, _window.y
    if pos_x == "center":
        text_position.centerx = _window.centerx
    elif pos_x == "right":
        text_position.right = _window.right
    if pos_y == "center":
        text_position.centery = _window.centery
    elif pos_y == "bottom":
        text_position.bottom = _window.bottom

    screen.blit(text, text_position)
    return text_position


class Menu:
    def __init__(
        self,
        screen: any,
        up_pos: Vector2,
        down_pos: Vector2,
        width: float,
        height: float,
        color: tuple,
        roundness: int,
        contents: list,
        slide_speed: float = 1,
        corners_rounded: tuple = (True, True, True, True),
        show: bool = True,
        render_at_end: bool = False,
    ) -> None:
        """
        up_pos: Where the menu is when its up
        down_pos: Where the menu is when its down
        width: How wide the menu is
        height: How tall the menu is
        color: Need I say it :/
        roundness: How rounded the corners are
        contents: All of the things in the menu
        slide_speed: How fast the menu slides into position
        corners_rounded: Which of the corners of the menu should be rounded (top left, top right, bottom left, bottom right)
        show: Whether the menu starts in the up or down position
        render_at_and: If the menu show always render or not
        """
        self.up_pos = Vector2(up_pos)
        self.width = width
        self.height = height
        self.down_pos = Vector2(down_pos)
        self.color = color
        self.roundness = roundness
        self.contents = contents
        self.corners_rounded = corners_rounded
        self.screen = screen
        if show == True:
            self.slide_progress = 1
            self.direct = 1
        else:
            self.slide_progress = 0
            self.direct = -1
        self.slide_speed = slide_speed
        self.render_at_end = render_at_end

        for i in self.contents:
            i.menu = self

        self.update()

    def update(self):
        """
        Will update the pos of the menu by the sliding direction, and update contents
        """
        self.slide_progress += self.direct * self.slide_speed
        self.slide_progress = min(max(self.slide_progress, 0), 1)
        self.pos = self.down_pos + (self.up_pos - self.down_pos) * self.slide_progress

        cusor = pg.SYSTEM_CURSOR_ARROW
        for i in self.contents:
            test = i.update()
            if not test == None:
                cusor = test
        if Rect(self.pos, [self.width, self.height]).collidepoint(pg.mouse.get_pos()):
            pg.mouse.set_system_cursor(cusor)

    def render(self):
        """
        Renders the menu onto the screen
        """
        if not (self.slide_progress == 0 and not (self.render_at_end)):
            if not self.color == None:
                if self.corners_rounded[0]:
                    t_l = self.roundness
                else:
                    t_l = 0
                if self.corners_rounded[1]:
                    t_r = self.roundness
                else:
                    t_r = 0
                if self.corners_rounded[2]:
                    b_l = self.roundness
                else:
                    b_l = 0
                if self.corners_rounded[3]:
                    b_r = self.roundness
                else:
                    b_r = 0

                draw.rect(
                    self.screen,
                    self.color,
                    Rect(self.pos, [self.width, self.height]),
                    border_radius=self.roundness,
                    border_top_left_radius=t_l,
                    border_top_right_radius=t_r,
                    border_bottom_left_radius=b_l,
                    border_bottom_right_radius=b_r,
                )

            for i in self.contents:
                i.render()

    def pos_per(self, per: Vector2):
        """
        Gives out cords based on percentages of the menus position
        """
        return Vector2(
            self.pos.x + self.width * per[0], self.pos.y + self.height * per[1]
        )

    def event_process(self, even):
        """
        Has contents process events
        """
        for i in self.contents:
            i.event_process(even)

    def full_update(self, even):
        """
        Does all the actions you would to be done each frame, it also needs the event list
        """
        self.update()
        self.render()
        self.event_process(even)

    def focused(self):
        """
        Gives a bool on whether or not any Text objects are focused
        """
        for i in self.contents:
            if type(i) == Text:
                if i.focus:
                    return True
        return False

    def new_contents(self,new):
        self.contents = new
        for i in self.contents:
            i.menu = self

        self.update()



class Button:
    def __init__(
        self,
        icon: list,
        colors: tuple,
        pos: Vector2,
        size: Vector2,
        action,
        clicked: str,
        roundness: int = 0,
        show=True,
        has_func_arg: bool = False,
        fucn_arg: any = None,
        text_pos: list = 0,
    ) -> None:
        """
        icon: The icon of the button [[x%,y%],[x%,y%] ...] (copy and paste from icon maker)
        colors: ( color of the button backgroud, color of the button icon )
        pos: Percentage position on a menu [x%,y%]
        size: [width%, height%]
        show: If the button should be rendered
        action: The function to be called when the button clicked
        clicked: Whether the button's function is to be 'press', or 'held'
        roundness: How rounded the corners are
        has_func_arg: Whether the action function neeeds an arguement
        fucn_arg: What that arguement is
        text_pos: If the text will be ('right', 'left', 'center' x, 'top', 'bottom', 'center' y), if none is given it will be the default
        """

        self.has_func_arg = has_func_arg
        if has_func_arg:
            self.func_arg = fucn_arg

        self.menu = None
        self.action = action
        self.click_type = clicked
        self.colors = colors
        self.roundness = roundness
        self.icon = icon
        self.pos = Vector2(pos)
        self.width_height = Vector2(size)
        self.show = show
        self.clicked = False
        self.font = None
        if text_pos == 0:
            self.text_pos = [default_text_pos_x, default_text_pos_y]
        else:
            self.text_pos = text_pos

    def update(self):
        """
        Updates whether the button is being clicked and does its action
        """
        if self.font == None:
            self.font = pg.font.Font(default_font, math.floor(self.scr_rect().h * text_box_size))
        was = self.clicked
        self.clicked = False
        set_cursor = None
        if self.scr_rect().collidepoint(pg.mouse.get_pos()):
            set_cursor = pg.SYSTEM_CURSOR_HAND
            if pg.mouse.get_pressed()[0]:
                self.clicked = True
        if self.click_type == "held":
            if self.clicked:
                if self.has_func_arg:
                    self.action(self.func_arg)
                else:
                    self.action()
        elif self.click_type == "press":
            if (not was) and (self.clicked):
                if self.has_func_arg:
                    self.action(self.func_arg)
                else:
                    self.action()
        return set_cursor

    def render(self):
        if self.show:
            if type(self.icon) != list or type(self.icon) != tuple:
                self.icon = str(self.icon)
                draw_text_box(
                    self.menu.screen,
                    self.scr_rect(),
                    self.icon,
                    self.roundness,
                    self.colors[1],
                    self.colors[0],
                    self.font,
                    not (self.colors[0] == None),
                    self.text_pos[0],
                    self.text_pos[1],
                )
            else:
                draw.rect(
                    self.menu.screen,
                    self.colors[0],
                    self.scr_rect(),
                    border_radius=self.roundness,
                )
                for i in self.icon:
                    draw.polygon(
                        self.menu.screen, self.colors[1], [self.pos_per(x) for x in i]
                    )

    def pos_per(self, per):
        """
        Gives out cords based on percentages of the buttons position
        """
        real_rect = self.scr_rect()
        return Vector2(
            real_rect.x + real_rect.w * per[0], real_rect.y + real_rect.h * per[1]
        )

    def scr_rect(self):
        """
        Gives a pygame Rect of the button on the screen
        """
        return Rect(
            self.menu.pos_per(self.pos),
            [
                self.width_height[0] * self.menu.width,
                self.width_height[1] * self.menu.height,
            ],
        )

    def event_process(self, even):
        """
        Pst... this does NOTHING!
        """
        pass


class Slider:
    def __init__(
        self,
        icon: list,
        colors: tuple,
        pos: Vector2,
        size: Vector2,
        action,
        roundness: int = 0,
        show=True,
        text_pos: list = 0,
    ) -> None:
        """
        icon: The icon of the slider [[x%,y%],[x%,y%] ...] (copy and paste from icon maker)
        colors: ( color of the slider backgroud, color of the slider icon, color of the slider knob )
        pos: Percentage position on a menu [x%,y%]
        size: [width%, height%]
        show: If the slider should be rendered
        action: The function to be called when the slider is changed, should give an output for the value of the knob when the 'get' key word is passed
        roundness: How rounded the corners are
        text_pos: If the text will be ('right', 'left', 'center' x, 'top', 'bottom', 'center' y), if none is given it will be the default
        """

        self.menu = None
        self.action = action
        self.colors = colors
        self.roundness = roundness
        self.icon = icon
        self.pos = Vector2(pos)
        self.width_height = Vector2(size)
        self.show = show
        self.knob_progress = action("get")
        self.font = None
        if text_pos == 0:
            self.text_pos = [default_text_pos_x, default_text_pos_y]
        else:
            self.text_pos = text_pos

    def update(self):
        """
        Updates the slider, called by parent menu
        """
        if self.font == None:
            self.font = pg.font.Font(default_font, math.floor(self.scr_rect().h * text_box_size))
        set_cursor = None
        if self.scr_rect().collidepoint(pg.mouse.get_pos()):
            set_cursor = pg.SYSTEM_CURSOR_HAND
            if pg.mouse.get_pressed()[0]:
                self.knob_progress = min(
                    max(self.x_to_knob(pg.mouse.get_pos()[0]), 0), 1
                )
                self.action(self.knob_progress)
            else:
                self.knob_progress = min(max(self.action("get"), 0), 1)
        else:
            self.knob_progress = min(max(self.action("get"), 0), 1)
        return set_cursor

    def render(self):
        if self.show:
            # Box
            if type(self.icon) != list or type(self.icon) != tuple:
                self.icon = str(self.icon)
                draw.rect(
                    self.menu.screen,
                    self.colors[0],
                    self.scr_rect(),
                    border_radius=self.roundness,
                )
                draw_text_box(
                    self.menu.screen,
                    Rect(
                        self.scr_rect()[:3] + [self.scr_rect().h * slider_text_height]
                    ),
                    self.icon,
                    self.roundness,
                    self.colors[1],
                    self.colors[0],
                    self.font,
                    False,
                    self.text_pos[0],
                    self.text_pos[1],
                )
            else:
                draw.rect(
                    self.menu.screen,
                    self.colors[0],
                    self.scr_rect(),
                    border_radius=self.roundness,
                )
                for i in self.icon:
                    draw.polygon(
                        self.menu.screen, self.colors[1], [self.pos_per(x) for x in i]
                    )
            # Bar
            draw.line(
                self.menu.screen,
                self.colors[1],
                self.get_bar_pos()[0],
                self.get_bar_pos()[1],
                int(self.scr_rect().h * slider_bar_thickness),
            )
            draw.circle(
                self.menu.screen,
                self.colors[1],
                (self.get_bar_pos()[0].x, self.get_bar_pos()[0].y + 1),
                self.scr_rect().h * slider_bar_thickness / 2,
            )
            draw.circle(
                self.menu.screen,
                self.colors[1],
                (self.get_bar_pos()[1].x, self.get_bar_pos()[1].y + 1),
                self.scr_rect().h * slider_bar_thickness / 2,
            )
            # Knob
            draw.circle(
                self.menu.screen,
                self.colors[2],
                self.get_knob_pos(),
                self.scr_rect().h * slider_knob_size,
            )

    def get_bar_pos(self):
        """
        Gives the pos of the bar on the screen as ((x1,y1) , (x2,y2))
        """
        return (
            self.pos_per(((slider_bar_length + 1) / 2, slider_bar_height)),
            self.pos_per(((1 - slider_bar_length) / 2, slider_bar_height)),
        )

    def get_knob_pos(self):
        """
        Gives the position of the knob on the screen
        """
        return self.pos_per(
            (
                ((1 - slider_bar_length) / 2)
                + min(max(self.knob_progress, 0), 1) * slider_bar_length,
                slider_bar_height,
            )
        )

    def scr_rect(self):
        """
        Gives a pygame Rect of the button on the screen
        """
        return Rect(
            self.menu.pos_per(self.pos),
            [
                self.width_height[0] * self.menu.width,
                self.width_height[1] * self.menu.height,
            ],
        )

    def x_to_knob(self, x):
        """
        Gives the value that knob should be set to given the x
        """
        return (x - (self.get_bar_pos()[1].x)) / (self.scr_rect().w * slider_bar_length)

    def pos_per(self, per):
        """
        Gives out cords based on percentages of the buttons position
        """
        real_rect = self.scr_rect()
        return Vector2(
            real_rect.x + real_rect.w * per[0], real_rect.y + real_rect.h * per[1]
        )

    def event_process(self, even):
        """
        Pst... this does NOTHING!
        """
        pass


class Text:
    def __init__(
        self,
        text: str,
        colors: tuple,
        pos: Vector2,
        size: Vector2,
        editable: bool = True,
        roundness: int = 0,
        show=True,
        text_pos: list = 0,
    ) -> None:
        """
        text: The icon of the slider [[x%,y%],[x%,y%] ...] (copy and paste from icon maker)
        colors: ( color of the text backgroud, color of the text )
        pos: Percentage position on a menu [x%,y%]
        size: [width%, height%]
        show: If the display should be rendered
        roundness: How rounded the corners are
        text_pos: If the text will be ('right', 'left', 'center' x, 'top', 'bottom', 'center' y), if none is given it will be the default
        """

        self.menu = None
        self.colors = colors
        self.roundness = roundness
        self.text = text
        self.pos = Vector2(pos)
        self.width_height = Vector2(size)
        self.focus = False
        self.editable = editable
        self.focus_pos = 0
        self.show = show
        self.font = None
        if text_pos == 0:
            self.text_pos = [default_text_pos_x, default_text_pos_y]
        else:
            self.text_pos = text_pos

    def update(self):
        """
        Updates the text box
        """
        if self.font == None:
            self.font = pg.font.Font(default_font, math.floor(self.scr_rect().h * text_box_size))
        if self.editable:
            set_cursor = None
            if self.scr_rect().collidepoint(pg.mouse.get_pos()):
                set_cursor = pg.SYSTEM_CURSOR_IBEAM
            if pg.mouse.get_pressed()[0]:
                if self.scr_rect().collidepoint(pg.mouse.get_pos()):
                    self.focus = True
                    self.focus_pos = 0
                else:
                    self.focus = False
            return set_cursor

    def render(self):
        if self.show:
            text_box = draw_text_box(
                self.menu.screen,
                self.scr_rect(),
                self.text,
                self.roundness,
                self.colors[1],
                self.colors[0],
                self.font,
                not (self.colors[0] == None),
                self.text_pos[0],
                self.text_pos[1],
            )
            if self.focus:
                global text_focus_bar_tick
                text_focus_bar_tick += 1
                text_focus_bar_tick %= text_focus_bar_rate * 2
                if text_focus_bar_tick < text_focus_bar_rate:
                    if self.focus_pos == 0:
                        draw.line(
                            self.menu.screen,
                            self.colors[1],
                            text_box.topright,
                            text_box.bottomright,
                            int(self.scr_rect().h * text_focus_bar_w),
                        )
                    else:
                        rect = self.scr_rect()
                        font = pg.font.Font(
                            default_font, math.floor(rect.height * text_box_size)
                        )
                        text = font.render(
                            self.text[: self.focus_pos], False, (0, 0, 0), (0, 0, 0)
                        )
                        draw.line(
                            self.menu.screen,
                            self.colors[1],
                            (text.get_rect().w + text_box.x, text_box.y),
                            (text.get_rect().w + text_box.x, text_box.y + text_box.h),
                            int(rect.h * text_focus_bar_w),
                        )

    def scr_rect(self):
        """
        Gives a pygame Rect of the button on the screen
        """
        return Rect(
            self.menu.pos_per(self.pos),
            [
                self.width_height[0] * self.menu.width,
                self.width_height[1] * self.menu.height,
            ],
        )

    def pos_per(self, per):
        """
        Gives out cords based on percentages of the buttons position
        """
        real_rect = self.scr_rect()
        return Vector2(
            real_rect.x + real_rect.w * per[0], real_rect.y + real_rect.h * per[1]
        )

    def event_process(self, even):
        """
        Allows for the text to be edited
        """
        if self.editable:
            if self.focus:
                for event in even:
                    if event.type == pg.KEYDOWN:
                        global text_focus_bar_tick
                        text_focus_bar_tick = 0
                        if event.key == pg.K_RETURN:
                            self.text = ""
                        elif event.key == pg.K_BACKSPACE:
                            if self.focus_pos == 0:
                                self.text = self.text[:-1]
                            else:
                                self.text = (
                                    self.text[: self.focus_pos - 1]
                                    + self.text[self.focus_pos :]
                                )
                        elif event.key == pg.K_LEFT:
                            self.focus_pos -= 1
                            self.focus_pos = min(
                                max(self.focus_pos, -len(self.text)), 0
                            )
                        elif event.key == pg.K_RIGHT:
                            self.focus_pos += 1
                            self.focus_pos = min(
                                max(self.focus_pos, -len(self.text)), 0
                            )
                        else:
                            if self.focus_pos == 0:
                                self.text += event.unicode
                            else:
                                self.text = (
                                    self.text[: self.focus_pos]
                                    + event.unicode
                                    + self.text[self.focus_pos :]
                                )



class Toggle:
    def __init__(
        self,
        colors: tuple,
        pos: Vector2,
        size: Vector2,
        on: bool = False,
        show=True,
    ) -> None:
        """
        A switch that can be on or off

        colors: ( color of the toggle backgroud off, color of the toggle background on, color of the toggle switch )
        pos: Percentage position on a menu [x%,y%]
        size: [width%, height%]
        on: If it starts on or off
        show: If the toggle should be rendered
        """

        

        self.menu = None
        self.colors = colors
        self.pos = Vector2(pos)
        self.width_height = Vector2(size)
        self.show = show
        self.clicked = False
        self.on = on


    def update(self):
        """
        Updates whether the toggle has been switched
        """
        was = self.clicked
        self.clicked = False
        set_cursor = None
        if self.scr_rect().collidepoint(pg.mouse.get_pos()):
            set_cursor = pg.SYSTEM_CURSOR_HAND
            if pg.mouse.get_pressed()[0]:
                self.clicked = True

        if (not was) and (self.clicked):
            self.on = not self.on
        return set_cursor


    def render(self):
        if self.show:
            if self.on:
                draw.line(self.menu.screen,self.colors[1],self.pos_per((0,0.5)),self.pos_per((1,0.5)),round(self.width_height.y*2))
                draw.circle(self.menu.screen,self.colors[1],self.pos_per((0,0.5)),self.width_height.y)
                draw.circle(self.menu.screen,self.colors[1],self.pos_per((1,0.5)),self.width_height.y)
                draw.circle(self.menu.screen,self.colors[2],self.pos_per((1,0.5)),round(self.width_height.y*toggle_knob_size))
            else:
                draw.line(self.menu.screen,self.colors[0],self.pos_per((0,0.5)),self.pos_per((1,0.5)),round(self.width_height.y*2))
                draw.circle(self.menu.screen,self.colors[0],self.pos_per((0,0.5)),self.width_height.y)
                draw.circle(self.menu.screen,self.colors[0],self.pos_per((1,0.5)),self.width_height.y)
                draw.circle(self.menu.screen,self.colors[2],self.pos_per((0,0.5)),round(self.width_height.y*toggle_knob_size))



    def pos_per(self, per):
        """
        Gives out cords based on percentages of the buttons position
        """
        real_rect = self.scr_rect()
        return Vector2(
            real_rect.x + real_rect.w * per[0], real_rect.y + real_rect.h * per[1]
        )

    def scr_rect(self):
        """
        Gives a pygame Rect of the button on the screen
        """
        return Rect(
            self.menu.pos_per(self.pos),
            [
                self.width_height[0] * self.menu.width,
                self.width_height[1] * self.menu.height,
            ],
        )

    def event_process(self, even):
        """
        Pst... this does NOTHING!
        """
        pass





ex_slider_var = 0


def ex_slider_func(set_get):
    global ex_slider_var
    var_min = -1
    var_max = 2

    if set_get == "get":
        return (ex_slider_var - var_min) / (var_max - var_min)
    else:
        ex_slider_var = var_min + ((var_max - var_min) * set_get)