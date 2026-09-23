    def dropna(self: ArrowExtensionArrayT) -> ArrowExtensionArrayT:
        """
        Return ArrowExtensionArray without NA values.

        Returns
        -------
        ArrowExtensionArray
        """
        return type(self)(pc.drop_null(self._data))
