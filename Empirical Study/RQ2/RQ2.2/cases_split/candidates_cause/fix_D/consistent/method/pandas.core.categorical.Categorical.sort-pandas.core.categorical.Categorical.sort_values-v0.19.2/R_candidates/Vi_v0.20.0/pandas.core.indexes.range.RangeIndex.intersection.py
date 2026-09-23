    def intersection(self, other):
        """
        Form the intersection of two Index objects. Sortedness of the result is
        not guaranteed

        Parameters
        ----------
        other : Index or array-like

        Returns
        -------
        intersection : Index
        """
        if not isinstance(other, RangeIndex):
            return super(RangeIndex, self).intersection(other)

        if not len(self) or not len(other):
            return RangeIndex._simple_new(None)

        # check whether intervals intersect
        # deals with in- and decreasing ranges
        int_low = max(min(self._start, self._stop + 1),
                      min(other._start, other._stop + 1))
        int_high = min(max(self._stop, self._start + 1),
                       max(other._stop, other._start + 1))
        if int_high <= int_low:
            return RangeIndex._simple_new(None)

        # Method hint: linear Diophantine equation
        # solve intersection problem
        # performance hint: for identical step sizes, could use
        # cheaper alternative
        gcd, s, t = self._extended_gcd(self._step, other._step)

        # check whether element sets intersect
        if (self._start - other._start) % gcd:
            return RangeIndex._simple_new(None)

        # calculate parameters for the RangeIndex describing the
        # intersection disregarding the lower bounds
        tmp_start = self._start + (other._start - self._start) * \
            self._step // gcd * s
        new_step = self._step * other._step // gcd
        new_index = RangeIndex(tmp_start, int_high, new_step, fastpath=True)

        # adjust index to limiting interval
        new_index._start = new_index._min_fitting_element(int_low)
        return new_index
