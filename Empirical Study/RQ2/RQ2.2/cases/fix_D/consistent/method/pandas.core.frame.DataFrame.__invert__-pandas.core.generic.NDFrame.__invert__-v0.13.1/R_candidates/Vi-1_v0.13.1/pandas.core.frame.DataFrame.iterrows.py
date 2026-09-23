    def iterrows(self):
        """
        Iterate over rows of DataFrame as (index, Series) pairs.

        Notes
        -----

        * ``iterrows`` does **not** preserve dtypes across the rows (dtypes
          are preserved across columns for DataFrames). For example,

            >>> df = DataFrame([[1, 1.0]], columns=['x', 'y'])
            >>> row = next(df.iterrows())[1]
            >>> print(row['x'].dtype)
            float64
            >>> print(df['x'].dtype)
            int64

        Returns
        -------
        it : generator
            A generator that iterates over the rows of the frame.
        """
        columns = self.columns
        for k, v in zip(self.index, self.values):
            s = Series(v, index=columns, name=k)
            yield k, s
