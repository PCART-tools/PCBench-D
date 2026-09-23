    @property
    def values(self):
        if self._tuples is not None:
            return self._tuples

        values = []
        for lev, lab in zip(self.levels, self.labels):
            # Need to box timestamps, etc.
            box = hasattr(lev, '_box_values')
            # Try to minimize boxing.
            if box and len(lev) > len(lab):
                taken = lev._box_values(com.take_1d(lev.values, lab))
            elif box:
                taken = com.take_1d(lev._box_values(lev.values), lab,
                                    fill_value=_get_na_value(lev.dtype.type))
            else:
                taken = com.take_1d(np.asarray(lev.values), lab)
            values.append(taken)

        self._tuples = lib.fast_zip(values)
        return self._tuples
