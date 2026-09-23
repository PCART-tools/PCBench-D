    @property
    @doc(DataFrame.dtypes.__doc__)
    def dtypes(self) -> Series:
        # error: Incompatible return value type (got "DataFrame", expected "Series")
        return self.apply(lambda df: df.dtypes)  # type: ignore[return-value]
