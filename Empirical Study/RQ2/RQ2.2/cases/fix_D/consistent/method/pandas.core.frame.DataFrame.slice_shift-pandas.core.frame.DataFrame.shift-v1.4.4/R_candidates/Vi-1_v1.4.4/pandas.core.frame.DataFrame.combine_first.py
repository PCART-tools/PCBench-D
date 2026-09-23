    def combine_first(self, other: DataFrame) -> DataFrame:
        """
        Update null elements with value in the same location in `other`.

        Combine two DataFrame objects by filling null values in one DataFrame
        with non-null values from other DataFrame. The row and column indexes
        of the resulting DataFrame will be the union of the two.

        Parameters
        ----------
        other : DataFrame
            Provided DataFrame to use to fill null values.

        Returns
        -------
        DataFrame
            The result of combining the provided DataFrame with the other object.

        See Also
        --------
        DataFrame.combine : Perform series-wise operation on two DataFrames
            using a given function.

        Examples
        --------
        >>> df1 = pd.DataFrame({'A': [None, 0], 'B': [None, 4]})
        >>> df2 = pd.DataFrame({'A': [1, 1], 'B': [3, 3]})
        >>> df1.combine_first(df2)
             A    B
        0  1.0  3.0
        1  0.0  4.0

        Null values still persist if the location of that null value
        does not exist in `other`

        >>> df1 = pd.DataFrame({'A': [None, 0], 'B': [4, None]})
        >>> df2 = pd.DataFrame({'B': [3, 3], 'C': [1, 1]}, index=[1, 2])
        >>> df1.combine_first(df2)
             A    B    C
        0  NaN  4.0  NaN
        1  0.0  3.0  1.0
        2  NaN  3.0  1.0
        """
        import pandas.core.computation.expressions as expressions

        def combiner(x, y):
            mask = extract_array(isna(x))

            x_values = extract_array(x, extract_numpy=True)
            y_values = extract_array(y, extract_numpy=True)

            # If the column y in other DataFrame is not in first DataFrame,
            # just return y_values.
            if y.name not in self.columns:
                return y_values

            return expressions.where(mask, y_values, x_values)

        combined = self.combine(other, combiner, overwrite=False)

        dtypes = {
            col: find_common_type([self.dtypes[col], other.dtypes[col]])
            for col in self.columns.intersection(other.columns)
            if not is_dtype_equal(combined.dtypes[col], self.dtypes[col])
        }

        if dtypes:
            combined = combined.astype(dtypes)

        return combined
