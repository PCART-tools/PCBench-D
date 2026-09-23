    def asof_locs(
        self, where: Index, mask: npt.NDArray[np.bool_]
    ) -> npt.NDArray[np.intp]:
        """
        Return the locations (indices) of labels in the index.

        As in the :meth:`pandas.Index.asof`, if the label (a particular entry in
        ``where``) is not in the index, the latest index label up to the
        passed label is chosen and its index returned.

        If all of the labels in the index are later than a label in ``where``,
        -1 is returned.

        ``mask`` is used to ignore ``NA`` values in the index during calculation.

        Parameters
        ----------
        where : Index
            An Index consisting of an array of timestamps.
        mask : np.ndarray[bool]
            Array of booleans denoting where values in the original
            data are not ``NA``.

        Returns
        -------
        np.ndarray[np.intp]
            An array of locations (indices) of the labels from the index
            which correspond to the return values of :meth:`pandas.Index.asof`
            for every element in ``where``.

        See Also
        --------
        Index.asof : Return the label from the index, or, if not present, the
            previous one.

        Examples
        --------
        >>> idx = pd.date_range('2023-06-01', periods=3, freq='D')
        >>> where = pd.DatetimeIndex(['2023-05-30 00:12:00', '2023-06-01 00:00:00',
        ...                           '2023-06-02 23:59:59'])
        >>> mask = np.ones(3, dtype=bool)
        >>> idx.asof_locs(where, mask)
        array([-1,  0,  1])

        We can use ``mask`` to ignore certain values in the index during calculation.

        >>> mask[1] = False
        >>> idx.asof_locs(where, mask)
        array([-1,  0,  0])
        """
        # error: No overload variant of "searchsorted" of "ndarray" matches argument
        # types "Union[ExtensionArray, ndarray[Any, Any]]", "str"
        # TODO: will be fixed when ExtensionArray.searchsorted() is fixed
        locs = self._values[mask].searchsorted(
            where._values, side="right"  # type: ignore[call-overload]
        )
        locs = np.where(locs > 0, locs - 1, 0)

        result = np.arange(len(self), dtype=np.intp)[mask].take(locs)

        first_value = self._values[mask.argmax()]
        result[(locs == 0) & (where._values < first_value)] = -1

        return result
