    def skew(
        self,
        axis: Axis | lib.NoDefault = lib.no_default,
        skipna: bool = True,
        numeric_only: bool = False,
        **kwargs,
    ) -> Series:
        """
        Return unbiased skew within groups.

        Normalized by N-1.

        Parameters
        ----------
        axis : {0 or 'index', 1 or 'columns', None}, default 0
            Axis for the function to be applied on.
            This parameter is only for compatibility with DataFrame and is unused.

        skipna : bool, default True
            Exclude NA/null values when computing the result.

        numeric_only : bool, default False
            Include only float, int, boolean columns. Not implemented for Series.

        **kwargs
            Additional keyword arguments to be passed to the function.

        Returns
        -------
        Series

        See Also
        --------
        Series.skew : Return unbiased skew over requested axis.

        Examples
        --------
        >>> ser = pd.Series([390., 350., 357., np.nan, 22., 20., 30.],
        ...                 index=['Falcon', 'Falcon', 'Falcon', 'Falcon',
        ...                        'Parrot', 'Parrot', 'Parrot'],
        ...                 name="Max Speed")
        >>> ser
        Falcon    390.0
        Falcon    350.0
        Falcon    357.0
        Falcon      NaN
        Parrot     22.0
        Parrot     20.0
        Parrot     30.0
        Name: Max Speed, dtype: float64
        >>> ser.groupby(level=0).skew()
        Falcon    1.525174
        Parrot    1.457863
        Name: Max Speed, dtype: float64
        >>> ser.groupby(level=0).skew(skipna=False)
        Falcon         NaN
        Parrot    1.457863
        Name: Max Speed, dtype: float64
        """
        result = self._op_via_apply(
            "skew",
            axis=axis,
            skipna=skipna,
            numeric_only=numeric_only,
            **kwargs,
        )
        return result
