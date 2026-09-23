    def idxmin(self, axis: Axis = 0, skipna: bool = True) -> Series:
        """
        Return index of first occurrence of minimum over requested axis.

        NA/null values are excluded.

        Parameters
        ----------
        axis : {0 or 'index', 1 or 'columns'}, default 0
            The axis to use. 0 or 'index' for row-wise, 1 or 'columns' for column-wise.
        skipna : bool, default True
            Exclude NA/null values. If an entire row/column is NA, the result
            will be NA.

        Returns
        -------
        Series
            Indexes of minima along the specified axis.

        Raises
        ------
        ValueError
            * If the row/column is empty

        See Also
        --------
        Series.idxmin : Return index of the minimum element.

        Notes
        -----
        This method is the DataFrame version of ``ndarray.argmin``.

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

        By default, it returns the index for the minimum value in each column.

        >>> df.idxmin()
        consumption                Pork
        co2_emissions    Wheat Products
        dtype: object

        To return the index for the minimum value in each row, use ``axis="columns"``.

        >>> df.idxmin(axis="columns")
        Pork                consumption
        Wheat Products    co2_emissions
        Beef                consumption
        dtype: object
        """
        axis = self._get_axis_number(axis)

        res = self._reduce(
            nanops.nanargmin, "argmin", axis=axis, skipna=skipna, numeric_only=False
        )
        indices = res._values

        # indices will always be np.ndarray since axis is not None and
        # values is a 2d array for DataFrame
        # error: Item "int" of "Union[int, Any]" has no attribute "__iter__"
        assert isinstance(indices, np.ndarray)  # for mypy

        index = self._get_axis(axis)
        result = [index[i] if i >= 0 else np.nan for i in indices]
        return self._constructor_sliced(result, index=self._get_agg_axis(axis))
