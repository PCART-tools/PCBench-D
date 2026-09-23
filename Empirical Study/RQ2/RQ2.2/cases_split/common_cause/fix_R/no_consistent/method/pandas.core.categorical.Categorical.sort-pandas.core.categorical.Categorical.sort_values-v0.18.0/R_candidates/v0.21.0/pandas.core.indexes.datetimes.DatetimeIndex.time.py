    @property
    def time(self):
        """
        Returns numpy array of datetime.time. The time part of the Timestamps.
        """
        return self._maybe_mask_results(libalgos.arrmap_object(
            self.asobject.values,
            lambda x: np.nan if x is libts.NaT else x.time()))
