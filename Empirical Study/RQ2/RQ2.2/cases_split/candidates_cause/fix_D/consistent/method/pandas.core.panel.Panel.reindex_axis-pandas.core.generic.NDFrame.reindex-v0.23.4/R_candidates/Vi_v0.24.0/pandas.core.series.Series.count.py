    def count(self, level=None):
        """
        Return number of non-NA/null observations in the Series.

        Parameters
        ----------
        level : int or level name, default None
            If the axis is a MultiIndex (hierarchical), count along a
            particular level, collapsing into a smaller Series

        Returns
        -------
        nobs : int or Series (if level specified)
        """
        if level is None:
            return notna(com.values_from_object(self)).sum()

        if isinstance(level, compat.string_types):
            level = self.index._get_level_number(level)

        lev = self.index.levels[level]
        level_codes = np.array(self.index.codes[level], subok=False, copy=True)

        mask = level_codes == -1
        if mask.any():
            level_codes[mask] = cnt = len(lev)
            lev = lev.insert(cnt, lev._na_value)

        obs = level_codes[notna(self.values)]
        out = np.bincount(obs, minlength=len(lev) or None)
        return self._constructor(out, index=lev,
                                 dtype='int64').__finalize__(self)
