import math
import time


class FPS:
    def __init__(
            self
    ) -> None:
        super(FPS, self).__init__()
        self.last_tick = 0
        self.delta = 0.0
        self.speed_hack = 1.0
        self.refresh()

    def refresh(self) -> None:
        self.last_tick = time.time()

    def tick(self) -> None:
        now = time.time()
        self.delta = (now - self.last_tick) * self.speed_hack
        self.last_tick = now

    def get_fps(self) -> float:
        try:
            return self.speed_hack / self.delta
        except ZeroDivisionError:
            return math.inf


class Timer:
    def __init__(
            self,
            timeout: float,
            repeat: bool = True,
            auto_run: bool = True,
            first_call: bool = False
    ) -> None:
        super(Timer, self).__init__()
        self.counter = 0.0
        self.timeout = timeout
        self.is_enabled = False
        self.repeat = repeat
        self.first_call = first_call
        if auto_run:
            self.run()

    def on_tick(self) -> None:
        pass

    def tick(self, delta: float) -> None:
        if not self.is_enabled:
            return
        self.counter += delta
        while self.counter >= self.timeout:
            self.is_enabled = self.repeat
            self.counter -= self.timeout
            self.on_tick()

    def stop(self) -> None:
        self.is_enabled = False
        self.counter = 0.0

    def run(self) -> None:
        self.is_enabled = True
        self.counter = 0.0
        if self.first_call:
            self.on_tick()

    def pause(self) -> None:
        self.is_enabled = False

    def resume(self) -> None:
        self.is_enabled = True
