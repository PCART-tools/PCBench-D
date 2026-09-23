    def _mode(self: ExtensionArrayT, dropna: bool = True) -> ExtensionArrayT:
        """
        Returns the mode(s) of the ExtensionArray.

        Always returns `ExtensionArray` even if only one value.

        Parameters
        ----------
        dropna : bool, default True
            Don't consider counts of NA values.

        Returns
        -------
        same type as self
            Sorted, if possible.
        """
        # error: Incompatible return value type (got "Union[ExtensionArray,
        # ndarray[Any, Any]]", expected "ExtensionArrayT")
        return mode(self, dropna=dropna)  # type: ignore[return-value]
