"""Module defining Application class."""
import os
import time
import pygame

_CURRENT_MENU = None
_OLD_MENUS = [_CURRENT_MENU]
_CURRENT_APPLICATION = None
_SCREEN = None

DEBUG_MODE = False
SHOW_FPS = False
TICK_BUSY = False

USE_IMG_DICT = True
_loaded = {}

class Application(object):
    """An Application object handles the pygame variables needed to create a
    graphical program, such as screen, screen's size window caption and window
    location.
    """

    def __init__(self, size, caption=None, icon="thorpy", center=True, flags=0):
        """This object handles the pygame variables needed to create a graphical
        program, such as screen, screen's size window caption and window
        location.

        <size> : a 2-sequence containing the size in pixels of the window to
        create.

        <caption> : the caption of the window. None means no caption.

        <icon> : path to the the icon image of the window.
            'thorpy' : default thorpy icon
            'pygame' : default pygame icon
            None : no icon

        <center> : centers the window on the computer screen.

        <flags> : flags passed to the pygame display surface. They can be:
            pygame.FULLSCREEN    create a fullscreen display
            pygame.DOUBLEBUF     recommended for HWSURFACE or OPENGL
            pygame.HWSURFACE     hardware accelerated, only in FULLSCREEN
            pygame.OPENGL        create an OpenGL renderable display
            pygame.RESIZABLE     display window should be sizeable
            pygame.NOFRAME       display window will have no border or controls
        """
        global _SCREEN, _CURRENT_APPLICATION
        _CURRENT_APPLICATION = self
        self.size = tuple(size)
        self.caption = caption
        pygame.init()
        if center:
            os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.set_icon(icon)
        screen = pygame.display.set_mode(self.size, flags)
        if self.caption:
            pygame.display.set_caption(caption)
        _SCREEN = screen
        self.default_path = "./"

    def set_icon(self, icon):
        if icon.lower() == "pygame":
            pass
        elif icon.lower() == "thorpy":
            from thorpy.miscgui.style import DEFAULT_ICON
            icon_surf = pygame.image.load(DEFAULT_ICON)
            pygame.display.set_icon(icon_surf)
        elif icon:
            icon_surf = load_image(DEFAULT_ICON)
            pygame.display.set_icon(icon_surf)
        else:
            icon_surf = pygame.Surface((1,1))
            icon_surf.set_colorkey((0,0,0))
            pygame.display.set_icon(icon_surf)

    def update(self):
        pygame.display.flip()

    def quit(self):
        pygame.font.quit()
        pygame.quit()

    def pause(self, fps=20):
        stay = True
        clock = pygame.time.Clock()
        while stay:
            clock.tick(fps)
            for e in pygame.event.get():
                if e.type == pygame.constants.QUIT:
                    pygame.font.quit()
                    pygame.quit()
                    exit()
                elif e.type == pygame.constants.KEYUP:
                    stay = False

    def save_screenshot(self, path=None, name=None, note=""):
        from thorpy.miscgui import functions
        if path is None:
            path = self.default_path
        if name is None:
            name = time.asctime().replace(" ", "_").replace(":", "-") + ".png"
        functions.debug_msg("Saving screenshot as " + path + note + name)
        pygame.image.save(functions.get_screen(), path+note+name)

    def get_statistics(self):
        from thorpy.elements.ghost import Ghost
        return {"number of elements":Ghost._current_id}
