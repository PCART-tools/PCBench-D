    @property
    def dtype(self) -> ExtensionDtype:
        """
        An instance of ExtensionDtype.

        Examples
        --------
        >>> pd.array([1, 2, 3]).dtype
        Int64Dtype()
        """
        raise AbstractMethodError(self)
