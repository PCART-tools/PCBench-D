    def _get_getitem_freq(self, key):
        """
        Find the `freq` attribute to assign to the result of a __getitem__ lookup.
        """
        is_period = is_period_dtype(self.dtype)
        if is_period:
            freq = self.freq
        else:
            freq = None
            if isinstance(key, slice):
                if self.freq is not None and key.step is not None:
                    freq = key.step * self.freq
                else:
                    freq = self.freq
            elif key is Ellipsis:
                # GH#21282 indexing with Ellipsis is similar to a full slice,
                #  should preserve `freq` attribute
                freq = self.freq
        return freq
