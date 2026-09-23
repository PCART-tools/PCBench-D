    def set_index(
        self,
        keys,
        *,
        drop: bool = True,
        append: bool = False,
        inplace: bool = False,
        verify_integrity: bool = False,
    ) -> DataFrame | None:
        """
        Set the DataFrame index using existing columns.

        Set the DataFrame index (row labels) using one or more existing
        columns or arrays (of the correct length). The index can replace the
        existing index or expand on it.

        Parameters
        ----------
        keys : label or array-like or list of labels/arrays
            This parameter can be either a single column key, a single array of
            the same length as the calling DataFrame, or a list containing an
            arbitrary combination of column keys and arrays. Here, "array"
            encompasses :class:`Series`, :class:`Index`, ``np.ndarray``, and
            instances of :class:`~collections.abc.Iterator`.
        drop : bool, default True
            Delete columns to be used as the new index.
        append : bool, default False
            Whether to append columns to existing index.
        inplace : bool, default False
            Whether to modify the DataFrame rather than creating a new one.
        verify_integrity : bool, default False
            Check the new index for duplicates. Otherwise defer the check until
            necessary. Setting to False will improve the performance of this
            method.

        Returns
        -------
        DataFrame or None
            Changed row labels or None if ``inplace=True``.

        See Also
        --------
        DataFrame.reset_index : Opposite of set_index.
        DataFrame.reindex : Change to new indices or expand indices.
        DataFrame.reindex_like : Change to same indices as other DataFrame.

        Examples
        --------
        >>> df = pd.DataFrame({'month': [1, 4, 7, 10],
        ...                    'year': [2012, 2014, 2013, 2014],
        ...                    'sale': [55, 40, 84, 31]})
        >>> df
           month  year  sale
        0      1  2012    55
        1      4  2014    40
        2      7  2013    84
        3     10  2014    31

        Set the index to become the 'month' column:

        >>> df.set_index('month')
               year  sale
        month
        1      2012    55
        4      2014    40
        7      2013    84
        10     2014    31

        Create a MultiIndex using columns 'year' and 'month':

        >>> df.set_index(['year', 'month'])
                    sale
        year  month
        2012  1     55
        2014  4     40
        2013  7     84
        2014  10    31

        Create a MultiIndex using an Index and a column:

        >>> df.set_index([pd.Index([1, 2, 3, 4]), 'year'])
                 month  sale
           year
        1  2012  1      55
        2  2014  4      40
        3  2013  7      84
        4  2014  10     31

        Create a MultiIndex using two Series:

        >>> s = pd.Series([1, 2, 3, 4])
        >>> df.set_index([s, s**2])
              month  year  sale
        1 1       1  2012    55
        2 4       4  2014    40
        3 9       7  2013    84
        4 16     10  2014    31
        """
        inplace = validate_bool_kwarg(inplace, "inplace")
        self._check_inplace_and_allows_duplicate_labels(inplace)
        if not isinstance(keys, list):
            keys = [keys]

        err_msg = (
            'The parameter "keys" may be a column key, one-dimensional '
            "array, or a list containing only valid column keys and "
            "one-dimensional arrays."
        )

        missing: list[Hashable] = []
        for col in keys:
            if isinstance(col, (Index, Series, np.ndarray, list, abc.Iterator)):
                # arrays are fine as long as they are one-dimensional
                # iterators get converted to list below
                if getattr(col, "ndim", 1) != 1:
                    raise ValueError(err_msg)
            else:
                # everything else gets tried as a key; see GH 24969
                try:
                    found = col in self.columns
                except TypeError as err:
                    raise TypeError(
                        f"{err_msg}. Received column of type {type(col)}"
                    ) from err
                else:
                    if not found:
                        missing.append(col)

        if missing:
            raise KeyError(f"None of {missing} are in the columns")

        if inplace:
            frame = self
        else:
            # GH 49473 Use "lazy copy" with Copy-on-Write
            frame = self.copy(deep=None)

        arrays: list[Index] = []
        names: list[Hashable] = []
        if append:
            names = list(self.index.names)
            if isinstance(self.index, MultiIndex):
                arrays.extend(
                    self.index._get_level_values(i) for i in range(self.index.nlevels)
                )
            else:
                arrays.append(self.index)

        to_remove: list[Hashable] = []
        for col in keys:
            if isinstance(col, MultiIndex):
                arrays.extend(col._get_level_values(n) for n in range(col.nlevels))
                names.extend(col.names)
            elif isinstance(col, (Index, Series)):
                # if Index then not MultiIndex (treated above)

                # error: Argument 1 to "append" of "list" has incompatible type
                #  "Union[Index, Series]"; expected "Index"
                arrays.append(col)  # type: ignore[arg-type]
                names.append(col.name)
            elif isinstance(col, (list, np.ndarray)):
                # error: Argument 1 to "append" of "list" has incompatible type
                # "Union[List[Any], ndarray]"; expected "Index"
                arrays.append(col)  # type: ignore[arg-type]
                names.append(None)
            elif isinstance(col, abc.Iterator):
                # error: Argument 1 to "append" of "list" has incompatible type
                # "List[Any]"; expected "Index"
                arrays.append(list(col))  # type: ignore[arg-type]
                names.append(None)
            # from here, col can only be a column label
            else:
                arrays.append(frame[col])
                names.append(col)
                if drop:
                    to_remove.append(col)

            if len(arrays[-1]) != len(self):
                # check newest element against length of calling frame, since
                # ensure_index_from_sequences would not raise for append=False.
                raise ValueError(
                    f"Length mismatch: Expected {len(self)} rows, "
                    f"received array of length {len(arrays[-1])}"
                )

        index = ensure_index_from_sequences(arrays, names)

        if verify_integrity and not index.is_unique:
            duplicates = index[index.duplicated()].unique()
            raise ValueError(f"Index has duplicate keys: {duplicates}")

        # use set to handle duplicate column names gracefully in case of drop
        for c in set(to_remove):
            del frame[c]

        # clear up memory usage
        index._cleanup()

        frame.index = index

        if not inplace:
            return frame
        return None
