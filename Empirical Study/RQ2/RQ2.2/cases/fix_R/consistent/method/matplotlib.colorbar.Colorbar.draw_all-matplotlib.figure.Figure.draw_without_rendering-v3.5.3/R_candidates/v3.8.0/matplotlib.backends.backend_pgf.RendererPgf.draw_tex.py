    def draw_tex(self, gc, x, y, s, prop, angle, *, mtext=None):
        # docstring inherited
        self.draw_text(gc, x, y, s, prop, angle, ismath="TeX", mtext=mtext)
