    def contains(self, mouseevent):
        # docstring inherited
        if self._different_canvas(mouseevent):
            return False, {}
        x, y = mouseevent.x, mouseevent.y
        try:
            trans = self.axes.transAxes.inverted()
            xaxes, yaxes = trans.transform((x, y))
        except ValueError:
            return False, {}
        (l, b), (r, t) = self.axes.transAxes.transform([(0, 0), (1, 1)])
        inaxis = 0 <= yaxes <= 1 and (
            l - self._pickradius < x < l or
            r < x < r + self._pickradius)
        return inaxis, {}
