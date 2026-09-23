    @deprecate_kwarg(old_arg_name='raise_conflict', new_arg_name='errors',
                     mapping={False: 'ignore', True: 'raise'})
    def update(self, other, join='left', overwrite=True, filter_func=None,
               errors='ignore'):
        """
        Modify Panel in place using non-NA values from other Panel.

        May also use object coercible to Panel. Will align on items.

        Parameters
        ----------
        other : Panel, or object coercible to Panel
            The object from which the caller will be udpated.
        join : {'left', 'right', 'outer', 'inner'}, default 'left'
            How individual DataFrames are joined.
        overwrite : bool, default True
            If True then overwrite values for common keys in the calling Panel.
        filter_func : callable(1d-array) -> 1d-array<bool>, default None
            Can choose to replace values other than NA. Return True for values
            that should be updated.
        errors : {'raise', 'ignore'}, default 'ignore'
            If 'raise', will raise an error if a DataFrame and other both.

            .. versionchanged :: 0.24.0
               Changed from `raise_conflict=False|True`
               to `errors='ignore'|'raise'`.

        See Also
        --------
        DataFrame.update : Similar method for DataFrames.
        dict.update : Similar method for dictionaries.
        """

        if not isinstance(other, self._constructor):
            other = self._constructor(other)

        axis_name = self._info_axis_name
        axis_values = self._info_axis
        other = other.reindex(**{axis_name: axis_values})

        for frame in axis_values:
            self[frame].update(other[frame], join=join, overwrite=overwrite,
                               filter_func=filter_func, errors=errors)
