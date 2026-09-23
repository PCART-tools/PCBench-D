    def draw_tex(self, gc, x, y, s, prop, angle, ismath='TeX!', mtext=None):
        # docstring inherited
        self._draw_text_as_path(gc, x, y, s, prop, angle, ismath="TeX")
