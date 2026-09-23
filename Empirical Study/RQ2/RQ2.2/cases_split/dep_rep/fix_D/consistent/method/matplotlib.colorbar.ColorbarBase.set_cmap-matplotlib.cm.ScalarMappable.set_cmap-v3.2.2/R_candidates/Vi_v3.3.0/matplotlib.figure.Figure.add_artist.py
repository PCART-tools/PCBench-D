    def add_artist(self, artist, clip=False):
        """
        Add an `.Artist` to the figure.

        Usually artists are added to axes objects using `.Axes.add_artist`;
        this method can be used in the rare cases where one needs to add
        artists directly to the figure instead.

        Parameters
        ----------
        artist : `~matplotlib.artist.Artist`
            The artist to add to the figure. If the added artist has no
            transform previously set, its transform will be set to
            ``figure.transFigure``.
        clip : bool, default: False
            Whether the added artist should be clipped by the figure patch.

        Returns
        -------
        `~matplotlib.artist.Artist`
            The added artist.
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
