    @property
    def date(self):
        """
        Returns numpy array of python datetime.date objects (namely, the date
        part of Timestamps without timezone information).
        """
        return self._maybe_mask_results(libalgos.arrmap_object(
            self.asobject.values, lambda x: x.date()))
