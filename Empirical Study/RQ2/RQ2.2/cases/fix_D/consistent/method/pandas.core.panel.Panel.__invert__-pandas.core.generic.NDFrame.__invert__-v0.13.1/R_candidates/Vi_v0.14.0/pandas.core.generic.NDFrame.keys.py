    def keys(self):
        """Get the 'info axis' (see Indexing for more)

        This is index for Series, columns for DataFrame and major_axis for
        Panel."""
        return self._info_axis
