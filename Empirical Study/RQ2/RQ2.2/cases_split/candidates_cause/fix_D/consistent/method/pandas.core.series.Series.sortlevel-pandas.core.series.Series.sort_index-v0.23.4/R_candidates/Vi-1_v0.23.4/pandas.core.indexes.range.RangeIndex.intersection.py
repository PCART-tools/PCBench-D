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

        first = self[::-1] if self._step < 0 else self
        second = other[::-1] if other._step < 0 else other

        # check whether intervals intersect
        # deals with in- and decreasing ranges
        int_low = max(first._start, second._start)
        int_high = min(first._stop, second._stop)
        if int_high <= int_low:
            return RangeIndex._simple_new(None)

        # Method hint: linear Diophantine equation
        # solve intersection problem
        # performance hint: for identical step sizes, could use
        # cheaper alternative
        gcd, s, t = first._extended_gcd(first._step, second._step)

        # check whether element sets intersect
        if (first._start - second._start) % gcd:
            return RangeIndex._simple_new(None)

        # calculate parameters for the RangeIndex describing the
        # intersection disregarding the lower bounds
        tmp_start = first._start + (second._start - first._start) * \
            first._step // gcd * s
        new_step = first._step * second._step // gcd
        new_index = RangeIndex(tmp_start, int_high, new_step, fastpath=True)

        # adjust index to limiting interval
        new_index._start = new_index._min_fitting_element(int_low)

        if (self._step < 0 and other._step < 0) is not (new_index._step < 0):
            new_index = new_index[::-1]
        return new_index
