    @classmethod
    def _from_pandas(
        cls,
        name: str,
        values: pd.Series[Any] | pd.DatetimeIndex,
        *,
        nan_to_null: bool = True,
    ) -> Self:
        """Construct a Series from a pandas Series or DatetimeIndex."""
        return cls._from_pyseries(
            pandas_to_pyseries(name, values, nan_to_null=nan_to_null)
        )
