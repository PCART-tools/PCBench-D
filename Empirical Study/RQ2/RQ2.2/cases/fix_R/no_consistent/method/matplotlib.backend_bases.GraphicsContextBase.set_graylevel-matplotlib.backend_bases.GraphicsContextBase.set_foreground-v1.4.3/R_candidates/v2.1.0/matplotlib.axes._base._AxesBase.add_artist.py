    def add_artist(self, a):
        """Add any :class:`~matplotlib.artist.Artist` to the axes.

        Use `add_artist` only for artists for which there is no dedicated
        "add" method; and if necessary, use a method such as
        `update_datalim` or `update_datalim_numerix` to manually update the
        dataLim if the artist is to be included in autoscaling.

        Returns the artist.
        """
        a.axes = self
        self.artists.append(a)
        self._set_artist_props(a)
        a.set_clip_path(self.patch)
        a._remove_method = lambda h: self.artists.remove(h)
        self.stale = True
        return a
