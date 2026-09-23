    def select_columns_by_name(self, names: list[str]) -> PandasDataFrameXchg:  # type: ignore[override]  # noqa: E501
        if not isinstance(names, abc.Sequence):
            raise ValueError("`names` is not a sequence")
        if not isinstance(names, list):
            names = list(names)

        return PandasDataFrameXchg(
            self._df.loc[:, names], self._nan_as_null, self._allow_copy
        )
