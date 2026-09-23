    def _draw_idle(self):
        if self.height() < 0 or self.width() < 0:
            self._draw_pending = False
        if not self._draw_pending:
            return
        try:
            self.draw()
        except Exception:
            # Uncaught exceptions are fatal for PyQt5, so catch them instead.
            traceback.print_exc()
        finally:
            self._draw_pending = False
