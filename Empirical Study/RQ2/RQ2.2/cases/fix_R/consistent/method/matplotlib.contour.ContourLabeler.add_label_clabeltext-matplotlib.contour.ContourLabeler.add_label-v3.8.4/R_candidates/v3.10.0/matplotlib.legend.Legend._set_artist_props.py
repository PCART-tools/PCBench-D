    def _set_artist_props(self, a):
        """
        Set the boilerplate props for artists added to Axes.
        """
        a.set_figure(self.get_figure(root=False))
        if self.isaxes:
            a.axes = self.axes

        a.set_transform(self.get_transform())
