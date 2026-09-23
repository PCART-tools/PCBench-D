    @cbook.deprecated('2.0', alternative='set_facecolor')
    def set_axis_bgcolor(self, color):
        """
        set the axes background color

        ACCEPTS: any matplotlib color - see
        :func:`~matplotlib.pyplot.colors`
        """
        return self.set_facecolor(color)
