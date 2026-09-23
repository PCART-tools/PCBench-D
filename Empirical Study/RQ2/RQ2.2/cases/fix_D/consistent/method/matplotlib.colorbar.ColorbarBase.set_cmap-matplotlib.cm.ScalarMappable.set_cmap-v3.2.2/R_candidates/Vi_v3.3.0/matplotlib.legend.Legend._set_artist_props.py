    def _set_artist_props(self, a):
        """
        Set the boilerplate props for artists added to axes.
        """
        a.set_figure(self.figure)
        if self.isaxes:
            # a.set_axes(self.axes)
            a.axes = self.axes

        a.set_transform(self.get_transform())
