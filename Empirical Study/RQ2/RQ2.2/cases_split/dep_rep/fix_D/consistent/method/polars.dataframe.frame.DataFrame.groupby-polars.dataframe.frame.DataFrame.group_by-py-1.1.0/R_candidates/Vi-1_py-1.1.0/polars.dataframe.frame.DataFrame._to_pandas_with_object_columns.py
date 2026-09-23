    def _to_pandas_with_object_columns(
        self,
        *,
        use_pyarrow_extension_array: bool,
        **kwargs: Any,
    ) -> pd.DataFrame:
        # Find which columns are of type pl.Object, and which aren't:
        object_columns = []
        not_object_columns = []
        for i, dtype in enumerate(self.dtypes):
            if dtype == Object:
                object_columns.append(i)
            else:
                not_object_columns.append(i)

        # Export columns that aren't pl.Object, in the same order:
        if not_object_columns:
            df_without_objects = self[:, not_object_columns]
            pandas_df = self._to_pandas_without_object_columns(
                df_without_objects,
                use_pyarrow_extension_array=use_pyarrow_extension_array,
                **kwargs,
            )
        else:
            pandas_df = pd.DataFrame()

        # Add columns that are pl.Object, using Series' custom to_pandas()
        # logic for this case. We do this in order, so the original index for
        # the next column in this dataframe is correct for the partially
        # constructed Pandas dataframe, since there are no additional or
        # missing columns to the inserted column's left.
        for i in object_columns:
            name = self.columns[i]
            pandas_df.insert(i, name, self.to_series(i).to_pandas())

        return pandas_df
