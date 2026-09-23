    def limit_range_for_scale(self, vmin, vmax, minpos):
        """
        Returns the range *vmin*, *vmax*, possibly limited to the
        domain supported by this scale.

        *minpos* should be the minimum positive value in the data.
         This is used by log scales to determine a minimum value.
        """
        return vmin, vmax
