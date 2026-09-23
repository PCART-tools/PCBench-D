    def _to_pandas_without_object_columns(
        self,
        df: DataFrame,
        *,
        use_pyarrow_extension_array: bool,
        **kwargs: Any,
    ) -> pd.DataFrame:
        if not df.width:  # Empty dataframe, cannot infer schema from batches
            return pd.DataFrame()

        record_batches = df._df.to_pandas()
        tbl = pa.Table.from_batches(record_batches)
        if use_pyarrow_extension_array:
            return tbl.to_pandas(
                self_destruct=True,
                split_blocks=True,
                types_mapper=lambda pa_dtype: pd.ArrowDtype(pa_dtype),
                **kwargs,
            )

        date_as_object = kwargs.pop("date_as_object", False)
        return tbl.to_pandas(date_as_object=date_as_object, **kwargs)
