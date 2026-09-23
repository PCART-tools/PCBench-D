    def destroy(self):
        # We need to clear any pending timers that never fired, otherwise
        # we get a memory leak from the timer callbacks holding a reference
        while self.canvas._timers:
            timer = self.canvas._timers.pop()
            timer.stop()
        super().destroy()
