    def count(self, level=None):
        """
        Return number of non-NA/null observations in the Series

        Parameters
        ----------
        level : int, default None
            If the axis is a MultiIndex (hierarchical), count along a
            particular level, collapsing into a smaller Series

        Returns
        -------
        nobs : int or Series (if level specified)
        """
        if level is not None:
            mask = notnull(self.values)

            if isinstance(level, compat.string_types):
                level = self.index._get_level_number(level)

            level_index = self.index.levels[level]

            if len(self) == 0:
                return self._constructor(0, index=level_index)\
                           .__finalize__(self)

            # call cython function
            max_bin = len(level_index)
            labels = com._ensure_int64(self.index.labels[level])
            counts = lib.count_level_1d(mask.view(pa.uint8),
                                        labels, max_bin)
            return self._constructor(counts,
                                     index=level_index).__finalize__(self)

        return notnull(_values_from_object(self)).sum()
