    def _get_index(self) -> Optional[np.ndarray]:
        """
        Return index as an ndarray.

        Returns
        -------
        None or ndarray
        """

        if self.is_freq_type:
            return self._on.asi8
        return None
