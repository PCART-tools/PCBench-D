    def contains(self, mouseevent):
        """Test whether the mouse event occurred in the y axis.

        Returns *True* | *False*
        """
        inside, info = self._default_contains(mouseevent)
        if inside is not None:
            return inside, info

        x, y = mouseevent.x, mouseevent.y
        try:
            trans = self.axes.transAxes.inverted()
            xaxes, yaxes = trans.transform((x, y))
        except ValueError:
            return False, {}
        (l, b), (r, t) = self.axes.transAxes.transform([(0, 0), (1, 1)])
        inaxis = 0 <= yaxes <= 1 and (
            l - self.pickradius < x < l or
            r < x < r + self.pickradius)
        return inaxis, {}
