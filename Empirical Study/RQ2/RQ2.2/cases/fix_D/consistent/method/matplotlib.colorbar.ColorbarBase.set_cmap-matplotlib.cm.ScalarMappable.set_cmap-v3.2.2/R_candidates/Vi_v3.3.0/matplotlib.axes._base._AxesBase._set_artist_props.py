    def _set_artist_props(self, a):
        """Set the boilerplate props for artists added to axes."""
        a.set_figure(self.figure)
        if not a.is_transform_set():
            a.set_transform(self.transData)

        a.axes = self
        if a.mouseover:
            self._mouseover_set.add(a)
