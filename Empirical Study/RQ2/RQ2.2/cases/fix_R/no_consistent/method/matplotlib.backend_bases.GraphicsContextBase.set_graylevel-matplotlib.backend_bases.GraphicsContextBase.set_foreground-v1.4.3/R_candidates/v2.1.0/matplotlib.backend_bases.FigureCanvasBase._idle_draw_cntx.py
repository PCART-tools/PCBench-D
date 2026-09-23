    @contextmanager
    def _idle_draw_cntx(self):
        self._is_idle_drawing = True
        yield
        self._is_idle_drawing = False
