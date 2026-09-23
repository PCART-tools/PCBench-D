    def __call__(self, df):
        """Callable for column selection to be used by a
        :class:`ColumnTransformer`.

        Parameters
        ----------
        df : dataframe of shape (n_features, n_samples)
            DataFrame to select columns from.
        """
        if not hasattr(df, "iloc"):
            raise ValueError(
                "make_column_selector can only be applied to pandas dataframes"
            )
        df_row = df.iloc[:1]
        if self.dtype_include is not None or self.dtype_exclude is not None:
            df_row = df_row.select_dtypes(
                include=self.dtype_include, exclude=self.dtype_exclude
            )
        cols = df_row.columns
        if self.pattern is not None:
            cols = cols[cols.str.contains(self.pattern, regex=True)]
        return cols.tolist()
