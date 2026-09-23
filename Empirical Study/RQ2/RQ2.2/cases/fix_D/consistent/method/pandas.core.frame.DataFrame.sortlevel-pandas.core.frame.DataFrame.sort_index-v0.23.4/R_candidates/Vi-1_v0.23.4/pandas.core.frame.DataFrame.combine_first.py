    def combine_first(self, other):
        """
        Combine two DataFrame objects and default to non-null values in frame
        calling the method. Result index columns will be the union of the
        respective indexes and columns

        Parameters
        ----------
        other : DataFrame

        Returns
        -------
        combined : DataFrame

        Examples
        --------
        df1's values prioritized, use values from df2 to fill holes:

        >>> df1 = pd.DataFrame([[1, np.nan]])
        >>> df2 = pd.DataFrame([[3, 4]])
        >>> df1.combine_first(df2)
           0    1
        0  1  4.0

        See Also
        --------
        DataFrame.combine : Perform series-wise operation on two DataFrames
            using a given function
        """
        import pandas.core.computation.expressions as expressions

        def combiner(x, y, needs_i8_conversion=False):
            x_values = x.values if hasattr(x, 'values') else x
            y_values = y.values if hasattr(y, 'values') else y
            if needs_i8_conversion:
                mask = isna(x)
                x_values = x_values.view('i8')
                y_values = y_values.view('i8')
            else:
                mask = isna(x_values)

            return expressions.where(mask, y_values, x_values)

        return self.combine(other, combiner, overwrite=False)
