    def contains(self, mouseevent):
        """Test whether the mouse event occurred in the y axis.

        Returns *True* | *False*
        """
        if self._contains is not None:
            return self._contains(self, mouseevent)

        x, y = mouseevent.x, mouseevent.y
        try:
            trans = self.axes.transAxes.inverted()
            xaxes, yaxes = trans.transform_point((x, y))
        except ValueError:
            return False, {}
        l, b = self.axes.transAxes.transform_point((0, 0))
        r, t = self.axes.transAxes.transform_point((1, 1))
        inaxis = 0 <= yaxes <= 1 and (
            l - self.pickradius < x < l or
            r < x < r + self.pickradius)
        return inaxis, {}
