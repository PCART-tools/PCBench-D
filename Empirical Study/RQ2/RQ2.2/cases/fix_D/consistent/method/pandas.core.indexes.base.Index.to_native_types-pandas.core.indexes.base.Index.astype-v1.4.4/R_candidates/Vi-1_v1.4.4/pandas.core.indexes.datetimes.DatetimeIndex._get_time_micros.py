    def _get_time_micros(self) -> np.ndarray:
        """
        Return the number of microseconds since midnight.

        Returns
        -------
        ndarray[int64_t]
        """
        values = self._data._local_timestamps()

        nanos = values % (24 * 3600 * 1_000_000_000)
        micros = nanos // 1000

        micros[self._isnan] = -1
        return micros
