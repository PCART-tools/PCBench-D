    def __draw_idle_agg(self, *args):
        if not self._agg_draw_pending:
            return
        if self.height() < 0 or self.width() < 0:
            self._agg_draw_pending = False
            return
        try:
            self.draw()
        except Exception:
            # Uncaught exceptions are fatal for PyQt5, so catch them instead.
            traceback.print_exc()
        finally:
            self._agg_draw_pending = False
