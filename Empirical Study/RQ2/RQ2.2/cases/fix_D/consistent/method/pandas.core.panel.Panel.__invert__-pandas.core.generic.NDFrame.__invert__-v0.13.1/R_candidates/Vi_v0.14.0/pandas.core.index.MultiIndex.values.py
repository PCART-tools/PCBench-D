    @property
    def values(self):
        if self._is_v2:
            return self.view(np.ndarray)
        else:
            if self._tuples is not None:
                return self._tuples

            values = []
            for lev, lab in zip(self.levels, self.labels):
                taken = com.take_1d(lev.values, lab)
                # Need to box timestamps, etc.
                if hasattr(lev, '_box_values'):
                    taken = lev._box_values(taken)
                values.append(taken)

            self._tuples = lib.fast_zip(values)
            return self._tuples
