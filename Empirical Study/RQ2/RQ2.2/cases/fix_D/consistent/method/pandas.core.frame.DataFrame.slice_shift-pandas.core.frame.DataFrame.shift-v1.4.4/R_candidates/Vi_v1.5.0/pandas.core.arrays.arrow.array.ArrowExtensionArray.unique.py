    def unique(self: ArrowExtensionArrayT) -> ArrowExtensionArrayT:
        """
        Compute the ArrowExtensionArray of unique values.

        Returns
        -------
        ArrowExtensionArray
        """
        if pa_version_under2p0:
            fallback_performancewarning(version="2")
            return super().unique()
        else:
            return type(self)(pc.unique(self._data))
