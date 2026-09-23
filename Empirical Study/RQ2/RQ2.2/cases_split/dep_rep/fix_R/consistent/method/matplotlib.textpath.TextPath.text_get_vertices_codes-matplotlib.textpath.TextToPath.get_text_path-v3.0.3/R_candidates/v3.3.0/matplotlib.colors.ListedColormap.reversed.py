    def reversed(self, name=None):
        """
        Return a reversed instance of the Colormap.

        Parameters
        ----------
        name : str, optional
            The name for the reversed colormap. If it's None the
            name will be the name of the parent colormap + "_r".

        Returns
        -------
        ListedColormap
            A reversed instance of the colormap.
        """
        if name is None:
            name = self.name + "_r"

        colors_r = list(reversed(self.colors))
        new_cmap = ListedColormap(colors_r, name=name, N=self.N)
        # Reverse the over/under values too
        new_cmap._rgba_over = self._rgba_under
        new_cmap._rgba_under = self._rgba_over
        new_cmap._rgba_bad = self._rgba_bad
        return new_cmap
