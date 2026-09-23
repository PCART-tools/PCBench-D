    def pivot(self, index=None, columns=None, values=None):
        """
        Reshape data (produce a "pivot" table) based on column values. Uses
        unique values from index / columns to form axes of the resulting
        DataFrame.

        Parameters
        ----------
        index : string or object, optional
            Column name to use to make new frame's index. If None, uses
            existing index.
        columns : string or object
            Column name to use to make new frame's columns
        values : string or object, optional
            Column name to use for populating new frame's values. If not
            specified, all remaining columns will be used and the result will
            have hierarchically indexed columns

        Returns
        -------
        pivoted : DataFrame

        See also
        --------
        DataFrame.pivot_table : generalization of pivot that can handle
            duplicate values for one index/column pair
        DataFrame.unstack : pivot based on the index values instead of a
            column

        Notes
        -----
        For finer-tuned control, see hierarchical indexing documentation along
        with the related stack/unstack methods

        Examples
        --------

        >>> df = pd.DataFrame({'foo': ['one','one','one','two','two','two'],
                               'bar': ['A', 'B', 'C', 'A', 'B', 'C'],
                               'baz': [1, 2, 3, 4, 5, 6]})
        >>> df
            foo   bar  baz
        0   one   A    1
        1   one   B    2
        2   one   C    3
        3   two   A    4
        4   two   B    5
        5   two   C    6

        >>> df.pivot(index='foo', columns='bar', values='baz')
             A   B   C
        one  1   2   3
        two  4   5   6

        >>> df.pivot(index='foo', columns='bar')['baz']
             A   B   C
        one  1   2   3
        two  4   5   6


        """
        from pandas.core.reshape.reshape import pivot
        return pivot(self, index=index, columns=columns, values=values)
