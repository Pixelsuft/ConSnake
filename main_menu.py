import os
import fps_clock
import defines
import utils
import game
from pynput.keyboard import Key
from fmod_loader import sound_system, SOUND_MODE


class MainMenu:
    def __init__(
            self
    ) -> None:
        super(MainMenu, self).__init__()
        self.title = [_x[8:].replace(' ', ' ').replace('0', defines.BG_GREEN + ' ' + defines.BG_BLACK) for _x in '''
        0000000 00    0    0    0   0   0000000
        0       0 0   0   0 0   0  0    0      
        0000000 0  0  0  00000  00000   0000000
              0 0   0 0 0     0 0    0  0
        0000000 0    00 0     0 0     0 0000000'''.split('\n')[1:]]
        self.title_size = (39, 5)
        self.text = 'Press SPACE To Start, ESCape To Quit!'
        self.text_pos = [0, 0]
        self.text_bg = True
        self.text_timer = fps_clock.Timer(1)
        self.text_timer.on_tick = self.draw_text
        self.clock = fps_clock.FPS()
        self.size = utils.get_terminal_size()
        self.music = sound_system.create_sound(
            os.path.join(defines.CWD, 'sounds', 'Earthbound - Sanctuary Guardian.mp3'),
            SOUND_MODE
        )
        utils.keyboard_checkers.append(self)
        self.running = True
        self.channel = self.music.play()
        self.redraw()
        self.draw_text()
        self.clock.refresh()
        self.loop()

    def on_press(self, key: any) -> None:
        pass

    def on_release(self, key: any) -> None:
        if key == Key.space:
            self.running = False
            utils.scenes_to_load.append(game.Game)
            utils.scene_args.clear()
        elif key == Key.esc:
            self.running = False
            utils.scenes_to_load.clear()
            utils.scene_args.clear()

    def on_close(self) -> None:
        if self.channel.is_playing:
            self.channel.stop()

    def draw_text(self) -> None:
        if self.text_bg:
            self.text_bg = False
            print(utils.back(len(self.text)) + defines.BG_BLACK + defines.RED + self.text, end='')
        else:
            self.text_bg = True
            print(utils.back(len(self.text)) + defines.BG_RED + defines.GREEN + self.text, end='')

    def redraw(self) -> None:
        output = defines.BG_BLACK + defines.CLEAR + '\n'
        spaces_count = round(self.size[0] / 2 - self.title_size[0] / 2)
        for line in self.title:
            output += defines.BG_BLACK + ' ' * spaces_count + line + defines.BG_BLACK + '\n'
        output += '\n'
        self.text_pos[0] = round(self.size[0] / 2 - len(self.text) / 2)
        self.text_pos[1] = round((self.size[1] - self.title_size[1] - 2) / 2 - 0.5) + self.title_size[1] + 2
        for _ in range(self.size[1] - self.title_size[1] - 3):
            output += '\n'
        output += utils.pos(self.text_pos[0] + len(self.text.split('\n')[0]), self.text_pos[1])
        print(output, end='')

    def loop(self) -> None:
        while self.running:
            self.clock.tick()
            if not self.channel.is_playing and self.running:
                self.channel = self.music.play()
            term_size = utils.get_terminal_size()
            if not term_size == self.size:
                self.size = term_size
                self.redraw()
            self.text_timer.tick(self.clock.delta)
        self.on_close()
