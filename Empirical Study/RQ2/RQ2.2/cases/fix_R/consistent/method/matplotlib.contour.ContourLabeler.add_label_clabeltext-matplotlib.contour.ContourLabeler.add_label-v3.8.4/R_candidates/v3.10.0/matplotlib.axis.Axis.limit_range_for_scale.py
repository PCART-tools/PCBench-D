    def limit_range_for_scale(self, vmin, vmax):
        """
        Return the range *vmin*, *vmax*, restricted to the domain supported by the
        current scale.
        """
        return self._scale.limit_range_for_scale(vmin, vmax, self.get_minpos())
