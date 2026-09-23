    def total_seconds(self):
        """
        Total duration of each element expressed in seconds.

        .. versionadded:: 0.17.0
        """
        return Index(self._maybe_mask_results(1e-9 * self.asi8),
                     name=self.name)
