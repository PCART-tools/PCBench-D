    def append(self, other, ignore_index=False, verify_integrity=False):
        """
        Append rows of `other` to the end of this frame, returning a new
        object. Columns not in this frame are added as new columns.

        Parameters
        ----------
        other : DataFrame or Series/dict-like object, or list of these
            The data to append.
        ignore_index : boolean, default False
            If True, do not use the index labels.
        verify_integrity : boolean, default False
            If True, raise ValueError on creating index with duplicates.

        Returns
        -------
        appended : DataFrame

        Notes
        -----
        If a list of dict/series is passed and the keys are all contained in the
        DataFrame's index, the order of the columns in the resulting DataFrame
        will be unchanged.

        See also
        --------
        pandas.concat : General function to concatenate DataFrame, Series
            or Panel objects

        Examples
        --------

        >>> df = pd.DataFrame([[1, 2], [3, 4]], columns=list('AB'))
        >>> df
           A  B
        0  1  2
        1  3  4
        >>> df2 = pd.DataFrame([[5, 6], [7, 8]], columns=list('AB'))
        >>> df.append(df2)
           A  B
        0  1  2
        1  3  4
        0  5  6
        1  7  8

        With `ignore_index` set to True:

        >>> df.append(df2, ignore_index=True)
           A  B
        0  1  2
        1  3  4
        2  5  6
        3  7  8

        """
        if isinstance(other, (Series, dict)):
            if isinstance(other, dict):
                other = Series(other)
            if other.name is None and not ignore_index:
                raise TypeError('Can only append a Series if ignore_index=True'
                                ' or if the Series has a name')

            index = None if other.name is None else [other.name]
            combined_columns = self.columns.tolist() + self.columns.union(other.index).difference(self.columns).tolist()
            other = other.reindex(combined_columns, copy=False)
            other = DataFrame(other.values.reshape((1, len(other))),
                              index=index, columns=combined_columns).convert_objects()
            if not self.columns.equals(combined_columns):
                self = self.reindex(columns=combined_columns)
        elif isinstance(other, list) and not isinstance(other[0], DataFrame):
            other = DataFrame(other)
            if (self.columns.get_indexer(other.columns) >= 0).all():
                other = other.ix[:, self.columns]

        from pandas.tools.merge import concat
        if isinstance(other, (list, tuple)):
            to_concat = [self] + other
        else:
            to_concat = [self, other]
        return concat(to_concat, ignore_index=ignore_index,
                      verify_integrity=verify_integrity)
