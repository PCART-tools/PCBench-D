    def append(self, other, ignore_index=False, verify_integrity=False):
        """
        Append columns of other to end of this frame's columns and index,
        returning a new object.  Columns not in this frame are added as new
        columns.

        Parameters
        ----------
        other : DataFrame or list of Series/dict-like objects
        ignore_index : boolean, default False
            If True do not use the index labels. Useful for gluing together
            record arrays
        verify_integrity : boolean, default False
            If True, raise ValueError on creating index with duplicates

        Notes
        -----
        If a list of dict is passed and the keys are all contained in the
        DataFrame's index, the order of the columns in the resulting DataFrame
        will be unchanged

        Returns
        -------
        appended : DataFrame
        """
        if isinstance(other, (Series, dict)):
            if isinstance(other, dict):
                other = Series(other)
            if other.name is None and not ignore_index:
                raise TypeError('Can only append a Series if '
                                'ignore_index=True')

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
