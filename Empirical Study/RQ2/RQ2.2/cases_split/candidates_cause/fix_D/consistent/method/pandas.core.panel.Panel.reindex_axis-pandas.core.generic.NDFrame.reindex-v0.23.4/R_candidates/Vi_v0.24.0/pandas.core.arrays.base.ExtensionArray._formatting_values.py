    def _formatting_values(self):
        # type: () -> np.ndarray
        # At the moment, this has to be an array since we use result.dtype
        """
        An array of values to be printed in, e.g. the Series repr

        .. deprecated:: 0.24.0

           Use :meth:`ExtensionArray._formatter` instead.
        """
        return np.array(self)
