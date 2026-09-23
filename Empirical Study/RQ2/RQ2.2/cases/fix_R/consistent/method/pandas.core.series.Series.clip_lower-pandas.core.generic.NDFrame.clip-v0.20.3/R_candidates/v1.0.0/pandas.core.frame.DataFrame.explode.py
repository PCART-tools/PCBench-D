    def explode(self, column: Union[str, Tuple]) -> "DataFrame":
        """
        Transform each element of a list-like to a row, replicating index values.

        .. versionadded:: 0.25.0

        Parameters
        ----------
        column : str or tuple
            Column to explode.

        Returns
        -------
        DataFrame
            Exploded lists to rows of the subset columns;
            index will be duplicated for these rows.

        Raises
        ------
        ValueError :
            if columns of the frame are not unique.

        See Also
        --------
        DataFrame.unstack : Pivot a level of the (necessarily hierarchical)
            index labels.
        DataFrame.melt : Unpivot a DataFrame from wide format to long format.
        Series.explode : Explode a DataFrame from list-like columns to long format.

        Notes
        -----
        This routine will explode list-likes including lists, tuples,
        Series, and np.ndarray. The result dtype of the subset rows will
        be object. Scalars will be returned unchanged. Empty list-likes will
        result in a np.nan for that row.

        Examples
        --------
        >>> df = pd.DataFrame({'A': [[1, 2, 3], 'foo', [], [3, 4]], 'B': 1})
        >>> df
                   A  B
        0  [1, 2, 3]  1
        1        foo  1
        2         []  1
        3     [3, 4]  1

        >>> df.explode('A')
             A  B
        0    1  1
        0    2  1
        0    3  1
        1  foo  1
        2  NaN  1
        3    3  1
        3    4  1
        """

        if not (is_scalar(column) or isinstance(column, tuple)):
            raise ValueError("column must be a scalar")
        if not self.columns.is_unique:
            raise ValueError("columns must be unique")

        df = self.reset_index(drop=True)
        # TODO: use overload to refine return type of reset_index
        assert df is not None  # needed for mypy
        result = df[column].explode()
        result = df.drop([column], axis=1).join(result)
        result.index = self.index.take(result.index)
        result = result.reindex(columns=self.columns, copy=False)

        return result
