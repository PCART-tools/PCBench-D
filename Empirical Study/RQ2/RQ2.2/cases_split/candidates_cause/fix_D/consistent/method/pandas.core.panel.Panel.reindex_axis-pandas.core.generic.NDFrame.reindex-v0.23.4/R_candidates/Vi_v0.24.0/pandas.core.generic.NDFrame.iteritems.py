    def iteritems(self):
        """Iterate over (label, values) on info axis

        This is index for Series, columns for DataFrame, major_axis for Panel,
        and so on.
        """
        for h in self._info_axis:
            yield h, self[h]
