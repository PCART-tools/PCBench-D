    def _offset(self, ox, oy):
        'Move all the artists by ox,oy (axes coords)'

        for c in six.itervalues(self._cells):
            x, y = c.get_x(), c.get_y()
            c.set_x(x + ox)
            c.set_y(y + oy)
