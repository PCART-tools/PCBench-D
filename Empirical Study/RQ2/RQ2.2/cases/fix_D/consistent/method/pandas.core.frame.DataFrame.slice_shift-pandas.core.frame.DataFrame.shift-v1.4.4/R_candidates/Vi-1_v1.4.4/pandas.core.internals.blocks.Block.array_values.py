    @property
    def array_values(self) -> ExtensionArray:
        """
        The array that Series.array returns. Always an ExtensionArray.
        """
        # error: Argument 1 to "PandasArray" has incompatible type "Union[ndarray,
        # ExtensionArray]"; expected "Union[ndarray, PandasArray]"
        return PandasArray(self.values)  # type: ignore[arg-type]
