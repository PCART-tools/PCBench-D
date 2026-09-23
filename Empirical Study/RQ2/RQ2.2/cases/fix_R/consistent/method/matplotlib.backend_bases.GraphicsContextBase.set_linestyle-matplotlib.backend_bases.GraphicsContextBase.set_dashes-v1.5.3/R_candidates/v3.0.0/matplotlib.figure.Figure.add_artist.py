    def add_artist(self, artist, clip=False):
        """
        Add any :class:`~matplotlib.artist.Artist` to the figure.

        Usually artists are added to axes objects using
        :meth:`matplotlib.axes.Axes.add_artist`, but use this method in the
        rare cases that adding directly to the figure is necessary.

        Parameters
        ----------
        artist : `~matplotlib.artist.Artist`
            The artist to add to the figure. If the added artist has no
            transform previously set, its transform will be set to
            ``figure.transFigure``.
        clip : bool, optional, default ``False``
            An optional parameter ``clip`` determines whether the added artist
            should be clipped by the figure patch. Default is *False*,
            i.e. no clipping.

        Returns
        -------
        artist : The added `~matplotlib.artist.Artist`
        """
        artist.set_figure(self)
        self.artists.append(artist)
        artist._remove_method = self.artists.remove

        if not artist.is_transform_set():
            artist.set_transform(self.transFigure)

        if clip:
            artist.set_clip_path(self.patch)

        self.stale = True
        return artist
