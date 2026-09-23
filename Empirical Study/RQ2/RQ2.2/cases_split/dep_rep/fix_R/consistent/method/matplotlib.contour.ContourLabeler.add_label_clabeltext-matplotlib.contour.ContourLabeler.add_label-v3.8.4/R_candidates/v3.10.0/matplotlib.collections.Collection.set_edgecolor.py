    def set_edgecolor(self, c):
        """
        Set the edgecolor(s) of the collection.

        Parameters
        ----------
        c : :mpltype:`color` or list of :mpltype:`color` or 'face'
            The collection edgecolor(s).  If a sequence, the patches cycle
            through it.  If 'face', match the facecolor.
        """
        # We pass through a default value for use in LineCollection.
        # This allows us to maintain None as the default indicator in
        # _original_edgecolor.
        if isinstance(c, str) and c.lower() in ("none", "face"):
            c = c.lower()
        self._original_edgecolor = c
        self._set_edgecolor(c)
