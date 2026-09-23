    @property
    def dtype_counts(self) -> Mapping[str, int]:
        return _get_dataframe_dtype_counts(self.data)
