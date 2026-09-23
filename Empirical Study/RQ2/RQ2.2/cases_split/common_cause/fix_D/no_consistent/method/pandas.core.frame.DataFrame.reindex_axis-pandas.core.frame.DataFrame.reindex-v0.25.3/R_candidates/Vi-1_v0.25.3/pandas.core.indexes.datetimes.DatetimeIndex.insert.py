    def insert(self, loc, item):
        """
        Make new Index inserting new item at location

        Parameters
        ----------
        loc : int
        item : object
            if not either a Python datetime or a numpy integer-like, returned
            Index dtype will be object rather than datetime.

        Returns
        -------
        new_index : Index
        """
        if is_scalar(item) and isna(item):
            # GH 18295
            item = self._na_value

        freq = None

        if isinstance(item, (datetime, np.datetime64)):
            self._assert_can_do_op(item)
            if not self._has_same_tz(item) and not isna(item):
                raise ValueError("Passed item and index have different timezone")
            # check freq can be preserved on edge cases
            if self.size and self.freq is not None:
                if (loc == 0 or loc == -len(self)) and item + self.freq == self[0]:
                    freq = self.freq
                elif (loc == len(self)) and item - self.freq == self[-1]:
                    freq = self.freq
            item = _to_M8(item, tz=self.tz)

        try:
            new_dates = np.concatenate(
                (self[:loc].asi8, [item.view(np.int64)], self[loc:].asi8)
            )
            return self._shallow_copy(new_dates, freq=freq)
        except (AttributeError, TypeError):

            # fall back to object index
            if isinstance(item, str):
                return self.astype(object).insert(loc, item)
            raise TypeError("cannot insert DatetimeIndex with incompatible label")
