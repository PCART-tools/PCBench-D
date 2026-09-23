    def intersection(self, other, sort=False):
        """
        Form the intersection of two Index objects.

        Parameters
        ----------
        other : Index or array-like
        sort : False or None, default False
            Sort the resulting index if possible

            .. versionadded:: 0.24.0

            .. versionchanged:: 0.24.1

               Changed the default to ``False`` to match the behaviour
               from before 0.24.0.

        Returns
        -------
        intersection : Index
        """
        self._validate_sort_keyword(sort)

        if self.equals(other):
            return self._get_reconciled_name_object(other)

        if not isinstance(other, RangeIndex):
            return super().intersection(other, sort=sort)

        if not len(self) or not len(other):
            return self._simple_new(None)

        first = self._range[::-1] if self.step < 0 else self._range
        second = other._range[::-1] if other.step < 0 else other._range

        # check whether intervals intersect
        # deals with in- and decreasing ranges
        int_low = max(first.start, second.start)
        int_high = min(first.stop, second.stop)
        if int_high <= int_low:
            return self._simple_new(None)

        # Method hint: linear Diophantine equation
        # solve intersection problem
        # performance hint: for identical step sizes, could use
        # cheaper alternative
        gcd, s, t = self._extended_gcd(first.step, second.step)

        # check whether element sets intersect
        if (first.start - second.start) % gcd:
            return self._simple_new(None)

        # calculate parameters for the RangeIndex describing the
        # intersection disregarding the lower bounds
        tmp_start = first.start + (second.start - first.start) * first.step // gcd * s
        new_step = first.step * second.step // gcd
        new_range = range(tmp_start, int_high, new_step)
        new_index = self._simple_new(new_range)

        # adjust index to limiting interval
        new_start = new_index._min_fitting_element(int_low)
        new_range = range(new_start, new_index.stop, new_index.step)
        new_index = self._simple_new(new_range)

        if (self.step < 0 and other.step < 0) is not (new_index.step < 0):
            new_index = new_index[::-1]
        if sort is None:
            new_index = new_index.sort_values()
        return new_index
