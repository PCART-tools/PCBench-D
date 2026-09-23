    @property
    def dtype_counts(self) -> Mapping[str, int]:
        from pandas.core.frame import DataFrame

        return _get_dataframe_dtype_counts(DataFrame(self.data))
