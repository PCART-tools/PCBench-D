    def dropna(self: ArrowExtensionArrayT) -> ArrowExtensionArrayT:
        """
        Return ArrowExtensionArray without NA values.

        Returns
        -------
        ArrowExtensionArray
        """
        if pa_version_under6p0:
            fallback_performancewarning(version="6")
            return super().dropna()
        else:
            return type(self)(pc.drop_null(self._data))
