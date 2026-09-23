    @property
    def _data(self):
        """
        An int array that for performance reasons is created only when needed.

        The constructed array is saved in ``_cached_data``. This allows us to
        check if the array has been created without accessing ``_data`` and
        triggering the construction.
        """
        if self._cached_data is None:
            self._cached_data = np.arange(
                self.start, self.stop, self.step, dtype=np.int64
            )
        return self._cached_data
