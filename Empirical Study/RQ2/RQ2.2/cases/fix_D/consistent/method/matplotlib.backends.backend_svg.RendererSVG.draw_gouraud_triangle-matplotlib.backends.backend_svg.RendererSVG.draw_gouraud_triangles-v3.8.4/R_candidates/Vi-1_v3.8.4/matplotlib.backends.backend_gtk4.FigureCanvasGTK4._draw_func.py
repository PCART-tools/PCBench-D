    def _draw_func(self, drawing_area, ctx, width, height):
        self.on_draw_event(self, ctx)
        self._post_draw(self, ctx)
