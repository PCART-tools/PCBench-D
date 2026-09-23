    def _get_index(self, index=None):
        """
        Return index as ndarrays

        Returns
        -------
        tuple of (index, index_as_ndarray)
        """

        if self.is_freq_type:
            if index is None:
                index = self._on
            return index, index.asi8
        return index, index
