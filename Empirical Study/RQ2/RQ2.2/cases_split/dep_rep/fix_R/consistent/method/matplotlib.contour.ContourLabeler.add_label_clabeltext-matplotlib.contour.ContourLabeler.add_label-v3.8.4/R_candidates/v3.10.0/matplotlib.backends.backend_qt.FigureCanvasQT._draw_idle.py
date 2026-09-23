    def _draw_idle(self):
        with self._idle_draw_cntx():
            if not self._draw_pending:
                return
            self._draw_pending = False
            if self.height() <= 0 or self.width() <= 0:
                return
            try:
                self.draw()
            except Exception:
                # Uncaught exceptions are fatal for PyQt5, so catch them.
                traceback.print_exc()
