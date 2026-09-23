    def draw_idle(self):
        # docstring inherited
        if self._idle_draw_id:
            return

        def idle_draw(*args):
            try:
                self.draw()
            finally:
                self._idle_draw_id = None

        self._idle_draw_id = self._tkcanvas.after_idle(idle_draw)
