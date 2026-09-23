    def contains(self, mouseevent):
        """Test whether the mouse event occurred in the x axis.
        """
        if callable(self._contains):
            return self._contains(self, mouseevent)

        x, y = mouseevent.x, mouseevent.y
        try:
            trans = self.axes.transAxes.inverted()
            xaxes, yaxes = trans.transform_point((x, y))
        except ValueError:
            return False, {}
        l, b = self.axes.transAxes.transform_point((0, 0))
        r, t = self.axes.transAxes.transform_point((1, 1))
        inaxis = 0 <= xaxes <= 1 and (
            b - self.pickradius < y < b or
            t < y < t + self.pickradius)
        return inaxis, {}
