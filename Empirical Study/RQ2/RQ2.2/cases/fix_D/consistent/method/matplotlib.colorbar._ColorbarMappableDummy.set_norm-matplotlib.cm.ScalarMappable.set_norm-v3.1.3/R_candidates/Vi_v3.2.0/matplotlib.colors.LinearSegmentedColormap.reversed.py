    def reversed(self, name=None):
        """
        Make a reversed instance of the Colormap.

        Parameters
        ----------
        name : str, optional
            The name for the reversed colormap. If it's None the
            name will be the name of the parent colormap + "_r".

        Returns
        -------
        LinearSegmentedColormap
            The reversed colormap.
        """
        if name is None:
            name = self.name + "_r"

        # Using a partial object keeps the cmap picklable.
        data_r = {key: (functools.partial(self._reverser, data)
                        if callable(data) else
                        [(1.0 - x, y1, y0) for x, y0, y1 in reversed(data)])
                  for key, data in self._segmentdata.items()}

        return LinearSegmentedColormap(name, data_r, self.N, self._gamma)
