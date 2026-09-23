    def draw_idle(self):
        # docstring inherited
        if not self._idle:
            return

        self._idle = False

        def idle_draw(*args):
            try:
                self.draw()
            finally:
                self._idle = True

        self._idle_callback = self._tkcanvas.after_idle(idle_draw)
