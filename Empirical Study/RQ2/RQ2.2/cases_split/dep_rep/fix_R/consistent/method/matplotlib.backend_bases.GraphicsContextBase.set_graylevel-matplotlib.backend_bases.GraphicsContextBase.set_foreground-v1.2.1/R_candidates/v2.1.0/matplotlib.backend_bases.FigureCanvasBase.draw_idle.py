    def draw_idle(self, *args, **kwargs):
        """
        :meth:`draw` only if idle; defaults to draw but backends can override
        """
        if not self._is_idle_drawing:
            with self._idle_draw_cntx():
                self.draw(*args, **kwargs)
