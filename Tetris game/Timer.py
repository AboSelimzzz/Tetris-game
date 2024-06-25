from Constants import *


class Timer:
    def __init__(self, duration, repeated=False,func=None):
        self.duration = duration
        self.repeated = repeated
        self.func = func

        self.start = 0
        self.active = False

    def activate(self):
        self.active = True
        self.start = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False
        self.start = 0

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start >= self.duration:
            if self.active:
                # call func
                if self.func and self.start:
                    self.func()

                # reset timer
                self.deactivate()

                # to repeat
                if self.repeated:
                    self.activate()
