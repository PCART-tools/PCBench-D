    def set_index(self, keys, drop=True, append=False, inplace=False,
                  verify_integrity=False):
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
            encompasses :class:`Series`, :class:`Index` and ``np.ndarray``.
        drop : bool, default True
            Delete columns to be used as the new index.
        append : bool, default False
            Whether to append columns to existing index.
        inplace : bool, default False
            Modify the DataFrame in place (do not create a new object).
        verify_integrity : bool, default False
            Check the new index for duplicates. Otherwise defer the check until
            necessary. Setting to False will improve the performance of this
            method.

        Returns
        -------
        DataFrame
            Changed row labels.

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
        inplace = validate_bool_kwarg(inplace, 'inplace')

        err_msg = ('The parameter "keys" may be a column key, one-dimensional '
                   'array, or a list containing only valid column keys and '
                   'one-dimensional arrays.')

        if (is_scalar(keys) or isinstance(keys, tuple)
                or isinstance(keys, (ABCIndexClass, ABCSeries, np.ndarray))):
            # make sure we have a container of keys/arrays we can iterate over
            # tuples can appear as valid column keys!
            keys = [keys]
        elif not isinstance(keys, list):
            raise ValueError(err_msg)

        missing = []
        for col in keys:
            if (is_scalar(col) or isinstance(col, tuple)):
                # if col is a valid column key, everything is fine
                # tuples are always considered keys, never as list-likes
                if col not in self:
                    missing.append(col)
            elif (not isinstance(col, (ABCIndexClass, ABCSeries,
                                       np.ndarray, list))
                  or getattr(col, 'ndim', 1) > 1):
                raise ValueError(err_msg)

        if missing:
            raise KeyError('{}'.format(missing))

        if inplace:
            frame = self
        else:
            frame = self.copy()

        arrays = []
        names = []
        if append:
            names = [x for x in self.index.names]
            if isinstance(self.index, ABCMultiIndex):
                for i in range(self.index.nlevels):
                    arrays.append(self.index._get_level_values(i))
            else:
                arrays.append(self.index)

        to_remove = []
        for col in keys:
            if isinstance(col, ABCMultiIndex):
                for n in range(col.nlevels):
                    arrays.append(col._get_level_values(n))
                names.extend(col.names)
            elif isinstance(col, (ABCIndexClass, ABCSeries)):
                # if Index then not MultiIndex (treated above)
                arrays.append(col)
                names.append(col.name)
            elif isinstance(col, (list, np.ndarray)):
                arrays.append(col)
                names.append(None)
            # from here, col can only be a column label
            else:
                arrays.append(frame[col]._values)
                names.append(col)
                if drop:
                    to_remove.append(col)

        index = ensure_index_from_sequences(arrays, names)

        if verify_integrity and not index.is_unique:
            duplicates = index[index.duplicated()].unique()
            raise ValueError('Index has duplicate keys: {dup}'.format(
                dup=duplicates))

        # use set to handle duplicate column names gracefully in case of drop
        for c in set(to_remove):
            del frame[c]

        # clear up memory usage
        index._cleanup()

        frame.index = index

        if not inplace:
            return frame
