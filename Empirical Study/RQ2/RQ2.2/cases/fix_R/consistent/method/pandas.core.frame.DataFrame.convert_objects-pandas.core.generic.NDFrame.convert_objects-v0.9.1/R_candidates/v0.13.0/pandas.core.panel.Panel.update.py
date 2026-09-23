    def update(self, other, join='left', overwrite=True, filter_func=None,
               raise_conflict=False):
        """
        Modify Panel in place using non-NA values from passed
        Panel, or object coercible to Panel. Aligns on items

        Parameters
        ----------
        other : Panel, or object coercible to Panel
        join : How to join individual DataFrames
            {'left', 'right', 'outer', 'inner'}, default 'left'
        overwrite : boolean, default True
            If True then overwrite values for common keys in the calling panel
        filter_func : callable(1d-array) -> 1d-array<boolean>, default None
            Can choose to replace values other than NA. Return True for values
            that should be updated
        raise_conflict : bool
            If True, will raise an error if a DataFrame and other both
            contain data in the same place.
        """

        if not isinstance(other, self._constructor):
            other = self._constructor(other)

        axis_name = self._info_axis_name
        axis_values = self._info_axis
        other = other.reindex(**{axis_name: axis_values})

        for frame in axis_values:
            self[frame].update(other[frame], join, overwrite, filter_func,
                               raise_conflict)
