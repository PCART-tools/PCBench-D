    def delete(self, loc):
        """
        Make a new DatetimeIndex with passed location(s) deleted.

        Parameters
        ----------
        loc: int, slice or array of ints
            Indicate which sub-arrays to remove.

        Returns
        -------
        new_index : DatetimeIndex
        """
        new_dates = np.delete(self.asi8, loc)

        freq = None
        if is_integer(loc):
            if loc in (0, -len(self), -1, len(self) - 1):
                freq = self.freq
        else:
            if is_list_like(loc):
                loc = lib.maybe_indices_to_slice(
                    _ensure_int64(np.array(loc)), len(self))
            if isinstance(loc, slice) and loc.step in (1, None):
                if (loc.start in (0, None) or loc.stop in (len(self), None)):
                    freq = self.freq

        if self.tz is not None:
            new_dates = libts.tz_convert(new_dates, 'UTC', self.tz)
        return DatetimeIndex(new_dates, name=self.name, freq=freq, tz=self.tz)
