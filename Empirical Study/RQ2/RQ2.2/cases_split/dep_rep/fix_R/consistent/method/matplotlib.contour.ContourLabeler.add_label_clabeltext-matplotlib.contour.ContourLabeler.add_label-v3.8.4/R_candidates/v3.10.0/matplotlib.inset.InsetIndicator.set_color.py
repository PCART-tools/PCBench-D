    def set_color(self, c):
        """
        Set the edgecolor of the rectangle and the connectors, and the
        facecolor for the rectangle.

        Parameters
        ----------
        c : :mpltype:`color`
        """
        self._shared_setter('edgecolor', c)
        self._shared_setter('facecolor', c)
