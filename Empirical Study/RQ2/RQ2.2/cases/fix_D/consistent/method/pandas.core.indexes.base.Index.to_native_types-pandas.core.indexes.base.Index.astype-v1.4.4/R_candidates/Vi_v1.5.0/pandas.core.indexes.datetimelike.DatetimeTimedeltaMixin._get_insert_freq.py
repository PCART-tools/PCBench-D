    def _get_insert_freq(self, loc: int, item):
        """
        Find the `freq` for self.insert(loc, item).
        """
        value = self._data._validate_scalar(item)
        item = self._data._box_func(value)

        freq = None
        if self.freq is not None:
            # freq can be preserved on edge cases
            if self.size:
                if item is NaT:
                    pass
                elif (loc == 0 or loc == -len(self)) and item + self.freq == self[0]:
                    freq = self.freq
                elif (loc == len(self)) and item - self.freq == self[-1]:
                    freq = self.freq
            else:
                # Adding a single item to an empty index may preserve freq
                if isinstance(self.freq, Tick):
                    # all TimedeltaIndex cases go through here; is_on_offset
                    #  would raise TypeError
                    freq = self.freq
                elif self.freq.is_on_offset(item):
                    freq = self.freq
        return freq
