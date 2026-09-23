    def insert(self, loc, item):
        """
        Make new Index inserting new item at location

        Parameters
        ----------
        loc : int
        item : object
            If not either a Python datetime or a numpy integer-like, returned
            Index dtype will be object rather than datetime.

        Returns
        -------
        new_index : Index
        """
        # try to convert if possible
        if isinstance(item, self._data._recognized_scalars):
            item = self._data._scalar_type(item)
        elif is_valid_nat_for_dtype(item, self.dtype):
            # GH 18295
            item = self._na_value
        elif is_scalar(item) and isna(item):
            # i.e. datetime64("NaT")
            raise TypeError(
                f"cannot insert {type(self).__name__} with incompatible label"
            )

        freq = None
        if isinstance(item, self._data._scalar_type) or item is NaT:
            self._data._check_compatible_with(item, setitem=True)

            # check freq can be preserved on edge cases
            if self.size and self.freq is not None:
                if item is NaT:
                    pass
                elif (loc == 0 or loc == -len(self)) and item + self.freq == self[0]:
                    freq = self.freq
                elif (loc == len(self)) and item - self.freq == self[-1]:
                    freq = self.freq
            item = item.asm8

        try:
            new_i8s = np.concatenate(
                (self[:loc].asi8, [item.view(np.int64)], self[loc:].asi8)
            )
            return self._shallow_copy(new_i8s, freq=freq)
        except (AttributeError, TypeError):

            # fall back to object index
            if isinstance(item, str):
                return self.astype(object).insert(loc, item)
            raise TypeError(
                f"cannot insert {type(self).__name__} with incompatible label"
            )
