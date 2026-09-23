    def idxmax(
        self,
        axis: Axis | None | lib.NoDefault = lib.no_default,
        skipna: bool = True,
        numeric_only: bool = False,
    ) -> DataFrame:
        """
        Return index of first occurrence of maximum over requested axis.

        NA/null values are excluded.

        Parameters
        ----------
        axis : {{0 or 'index', 1 or 'columns'}}, default None
            The axis to use. 0 or 'index' for row-wise, 1 or 'columns' for column-wise.
            If axis is not provided, grouper's axis is used.

            .. versionchanged:: 2.0.0

            .. deprecated:: 2.1.0
                For axis=1, operate on the underlying object instead. Otherwise
                the axis keyword is not necessary.

        skipna : bool, default True
            Exclude NA/null values. If an entire row/column is NA, the result
            will be NA.
        numeric_only : bool, default False
            Include only `float`, `int` or `boolean` data.

            .. versionadded:: 1.5.0

        Returns
        -------
        Series
            Indexes of maxima along the specified axis.

        Raises
        ------
        ValueError
            * If the row/column is empty

        See Also
        --------
        Series.idxmax : Return index of the maximum element.

        Notes
        -----
        This method is the DataFrame version of ``ndarray.argmax``.

        Examples
        --------
        Consider a dataset containing food consumption in Argentina.

        >>> df = pd.DataFrame({'consumption': [10.51, 103.11, 55.48],
        ...                    'co2_emissions': [37.2, 19.66, 1712]},
        ...                    index=['Pork', 'Wheat Products', 'Beef'])

        >>> df
                        consumption  co2_emissions
        Pork                  10.51         37.20
        Wheat Products       103.11         19.66
        Beef                  55.48       1712.00

        By default, it returns the index for the maximum value in each column.

        >>> df.idxmax()
        consumption     Wheat Products
        co2_emissions             Beef
        dtype: object

        To return the index for the maximum value in each row, use ``axis="columns"``.

        >>> df.idxmax(axis="columns")
        Pork              co2_emissions
        Wheat Products     consumption
        Beef              co2_emissions
        dtype: object
        """
        if axis is not lib.no_default:
            if axis is None:
                axis = self.axis
            axis = self.obj._get_axis_number(axis)
            self._deprecate_axis(axis, "idxmax")
        else:
            axis = self.axis

        def func(df):
            return df.idxmax(axis=axis, skipna=skipna, numeric_only=numeric_only)

        func.__name__ = "idxmax"
        result = self._python_apply_general(
            func, self._obj_with_exclusions, not_indexed_same=True
        )
        return result.astype(self.obj.index.dtype) if result.empty else result
