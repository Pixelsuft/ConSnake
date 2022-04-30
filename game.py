import os
import random
import fps_clock
import defines
import utils
import main_menu
from pynput.keyboard import Key
from fmod_loader import sound_system, SOUND_MODE


class Game:
    def __init__(
            self
    ) -> None:
        super(Game, self).__init__()
        self.field = (78, 22)
        self.offset = [0, 0]
        self.apple = [0, 0]
        self.snake = [[4, 1], [3, 1], [2, 1], [1, 1]]
        self.place_apple()
        self.clock = fps_clock.FPS()
        self.size = utils.get_terminal_size()
        utils.keyboard_checkers.append(self)
        self.running = True
        self.score = 0
        self.dir_x = 1
        self.dir_y = 0
        self._dir_x = 1
        self._dir_y = 0
        self.min_timeout = 1.0
        self.max_timeout = 0.04
        self.timeout_change = 0.01
        self.death_sound = sound_system.create_sound(
            os.path.join(defines.CWD, 'sounds', 'fail.ogg'),
            SOUND_MODE
        )
        self.apple_sound = sound_system.create_sound(
            os.path.join(defines.CWD, 'sounds', 'apple.ogg'),
            SOUND_MODE
        )
        self.music = sound_system.create_sound(
            os.path.join(defines.CWD, 'sounds', 'Descent OST - Level 4.mp3'),
            SOUND_MODE
        )
        self.channel = self.music.play()
        self.frequency = self.channel.frequency
        self.game_timer = fps_clock.Timer(self.min_timeout)
        self.game_timer.on_tick = self.on_game_tick
        self.redraw()
        self.clock.refresh()
        self.loop()

    def on_press(self, key: any) -> None:
        if key == Key.up and not self._dir_y:
            self.dir_x = 0
            self.dir_y = -1
        elif key == Key.right and not self._dir_x:
            self.dir_x = 1
            self.dir_y = 0
        elif key == Key.down and not self._dir_y:
            self.dir_x = 0
            self.dir_y = 1
        elif key == Key.left and not self._dir_x:
            self.dir_x = -1
            self.dir_y = 0
        elif key == Key.tab:
            self.clock.speed_hack = 4.0

    def on_release(self, key: any) -> None:
        if key == Key.esc:
            self.running = False
            utils.scenes_to_load.clear()
            utils.scenes_to_load.append(main_menu.MainMenu)
            utils.scene_args.clear()
        elif key == Key.tab:
            self.clock.speed_hack = 1.0

    def on_close(self) -> None:
        if self.channel.is_playing:
            self.channel.stop()

    def on_game_tick(self) -> None:
        del_pos = self.snake.pop(-1)
        self._dir_x = self.dir_x
        self._dir_y = self.dir_y
        self.snake.insert(0, [self.snake[0][0] + self._dir_x, self.snake[0][1] + self._dir_y])
        output = utils.pos(del_pos[0] + self.offset[0] + 1, del_pos[1] + self.offset[1] + 1) + defines.BG_BLACK + ' '
        if self.apple == self.snake[0]:
            self.snake.append(del_pos)
            output = utils.pos(del_pos[0] + self.offset[0] + 1, del_pos[1] + self.offset[1] + 1)
            output += defines.BG_GREEN + ' '
            self.score += 1
            self.game_timer.timeout -= self.timeout_change
            if self.game_timer.timeout < self.max_timeout:
                self.game_timer.timeout = self.max_timeout
            self.apple_sound.play()
            self.channel.frequency = self.frequency * (
                (self.min_timeout - self.game_timer.timeout) / (self.min_timeout - self.max_timeout) * 0.25 + 1
            )
            self.place_apple()
            self.draw_score()
            self.draw_apple()
        output += utils.pos(self.snake[1][0] + self.offset[0] + 1, self.snake[1][1] + self.offset[1] + 1)
        output += defines.BG_GREEN + ' '
        output += utils.pos(self.snake[0][0] + self.offset[0] + 1, self.snake[0][1] + self.offset[1] + 1)
        output += defines.BG_RED + ' '
        print(output, end='')
        if self.snake[0] in self.snake[1:] or not (self.field[0] > self.snake[0][0] >= 0) or\
                not (self.field[1] > self.snake[0][1] >= 0):
            self.running = False
            utils.scenes_to_load.clear()
            utils.scenes_to_load.append(main_menu.MainMenu)
            utils.scene_args.clear()
            channel = self.death_sound.play()
            while channel.is_playing:
                pass

    def place_apple(self) -> None:
        pos = [random.randint(0, self.field[0] - 1), random.randint(0, self.field[1] - 1)]
        while pos in self.snake:
            pos = [random.randint(0, self.field[0] - 1), random.randint(0, self.field[1] - 1)]
        self.apple = pos

    def draw_score(self) -> None:
        text1 = f'Score: {self.score}'
        text2 = f'Speed:' \
                f' {round((self.min_timeout - self.game_timer.timeout) / (self.min_timeout - self.max_timeout) * 100)}%'
        output = utils.pos(*self.offset) + defines.BG_BLUE + defines.WHITE + text1
        output += ' ' * (self.field[0] - len(text1) - len(text2) + 2) + text2
        print(
            output,
            end=''
        )

    def draw_apple(self) -> None:
        print(
            f'{utils.pos(self.apple[0] + self.offset[0] + 1, self.apple[1] + self.offset[1] + 1)}{defines.BG_BLACK}'
            f'{defines.RED}{defines.CIRCLE}',
            end=''
        )

    def redraw(self) -> None:
        self.offset[0] = round(self.size[0] / 2 - self.field[0] / 2)
        self.offset[1] = round(self.size[1] / 2 - self.field[1] / 2)
        output = defines.BG_BLACK + defines.CLEAR + '\n' * (self.offset[1] - 1)
        output += ' ' * (self.offset[0] - 1) + defines.BG_BLUE + ' ' * (self.field[0] + 2) + defines.BG_BLACK + '\n'
        for _ in range(self.field[1]):
            output += ' ' * (self.offset[0] - 1) + defines.BG_BLUE + ' ' + defines.BG_BLACK + ' ' * self.field[0]
            output += defines.BG_BLUE + ' ' + defines.BG_BLACK + '\n'
        output += ' ' * (self.offset[0] - 1) + defines.BG_BLUE + ' ' * (self.field[0] + 2) + defines.BG_BLACK + '\n'
        output += utils.pos(self.snake[0][0] + self.offset[0] + 1, self.snake[0][1] + self.offset[1] + 1)
        output += defines.BG_RED + ' '
        for part in self.snake[1:]:
            output += utils.pos(part[0] + self.offset[0] + 1, part[1] + self.offset[1] + 1)
            output += defines.BG_GREEN + ' '
        print(output, end='')
        self.draw_score()
        self.draw_apple()

    def loop(self) -> None:
        while self.running:
            self.clock.tick()
            if not self.channel.is_playing:
                self.channel = self.music.play()
                self.channel.frequency = self.frequency * (
                    (self.min_timeout - self.game_timer.timeout) / (self.min_timeout - self.max_timeout) * 0.25 + 1
                )
            term_size = utils.get_terminal_size()
            if not term_size == self.size:
                self.size = term_size
                self.redraw()
            self.game_timer.tick(self.clock.delta)
        self.on_close()
