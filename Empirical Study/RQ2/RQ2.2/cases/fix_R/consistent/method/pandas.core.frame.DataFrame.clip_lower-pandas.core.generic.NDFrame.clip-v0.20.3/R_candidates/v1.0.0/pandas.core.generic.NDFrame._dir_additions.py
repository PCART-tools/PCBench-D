    def _dir_additions(self):
        """ add the string-like attributes from the info_axis.
        If info_axis is a MultiIndex, it's first level values are used.
        """
        additions = {
            c
            for c in self._info_axis.unique(level=0)[:100]
            if isinstance(c, str) and c.isidentifier()
        }
        return super()._dir_additions().union(additions)
