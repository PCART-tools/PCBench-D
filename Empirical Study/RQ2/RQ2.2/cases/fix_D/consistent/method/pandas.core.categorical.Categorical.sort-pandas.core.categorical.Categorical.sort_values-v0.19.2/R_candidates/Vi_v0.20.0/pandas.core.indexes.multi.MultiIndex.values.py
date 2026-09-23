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
                taken = lev._box_values(algos.take_1d(lev._values, lab))
            elif box:
                taken = algos.take_1d(lev._box_values(lev._values), lab,
                                      fill_value=_get_na_value(lev.dtype.type))
            else:
                taken = algos.take_1d(np.asarray(lev._values), lab)
            values.append(taken)

        self._tuples = lib.fast_zip(values)
        return self._tuples
