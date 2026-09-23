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
        # try to convert if possible
        if _is_convertible_to_td(item):
            try:
                item = Timedelta(item)
            except Exception:
                pass
        elif is_scalar(item) and isna(item):
            # GH 18295
            item = self._na_value

        freq = None
        if isinstance(item, Timedelta) or (is_scalar(item) and isna(item)):

            # check freq can be preserved on edge cases
            if self.freq is not None:
                if ((loc == 0 or loc == -len(self)) and
                        item + self.freq == self[0]):
                    freq = self.freq
                elif (loc == len(self)) and item - self.freq == self[-1]:
                    freq = self.freq
            item = Timedelta(item).asm8.view(_TD_DTYPE)

        try:
            new_tds = np.concatenate((self[:loc].asi8, [item.view(np.int64)],
                                      self[loc:].asi8))
            return self._shallow_copy(new_tds, freq=freq)

        except (AttributeError, TypeError):

            # fall back to object index
            if isinstance(item, compat.string_types):
                return self.astype(object).insert(loc, item)
            raise TypeError(
                "cannot insert TimedeltaIndex with incompatible label")
