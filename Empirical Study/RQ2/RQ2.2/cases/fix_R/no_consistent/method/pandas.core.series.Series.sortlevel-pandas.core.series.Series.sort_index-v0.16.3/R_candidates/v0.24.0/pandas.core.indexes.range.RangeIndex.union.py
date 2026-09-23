    def union(self, other):
        """
        Form the union of two Index objects and sorts if possible

        Parameters
        ----------
        other : Index or array-like

        Returns
        -------
        union : Index
        """
        self._assert_can_do_setop(other)
        if len(other) == 0 or self.equals(other) or len(self) == 0:
            return super(RangeIndex, self).union(other)

        if isinstance(other, RangeIndex):
            start_s, step_s = self._start, self._step
            end_s = self._start + self._step * (len(self) - 1)
            start_o, step_o = other._start, other._step
            end_o = other._start + other._step * (len(other) - 1)
            if self._step < 0:
                start_s, step_s, end_s = end_s, -step_s, start_s
            if other._step < 0:
                start_o, step_o, end_o = end_o, -step_o, start_o
            if len(self) == 1 and len(other) == 1:
                step_s = step_o = abs(self._start - other._start)
            elif len(self) == 1:
                step_s = step_o
            elif len(other) == 1:
                step_o = step_s
            start_r = min(start_s, start_o)
            end_r = max(end_s, end_o)
            if step_o == step_s:
                if ((start_s - start_o) % step_s == 0 and
                        (start_s - end_o) <= step_s and
                        (start_o - end_s) <= step_s):
                    return RangeIndex(start_r, end_r + step_s, step_s)
                if ((step_s % 2 == 0) and
                        (abs(start_s - start_o) <= step_s / 2) and
                        (abs(end_s - end_o) <= step_s / 2)):
                    return RangeIndex(start_r, end_r + step_s / 2, step_s / 2)
            elif step_o % step_s == 0:
                if ((start_o - start_s) % step_s == 0 and
                        (start_o + step_s >= start_s) and
                        (end_o - step_s <= end_s)):
                    return RangeIndex(start_r, end_r + step_s, step_s)
            elif step_s % step_o == 0:
                if ((start_s - start_o) % step_o == 0 and
                        (start_s + step_o >= start_o) and
                        (end_s - step_o <= end_o)):
                    return RangeIndex(start_r, end_r + step_o, step_o)

        return self._int64index.union(other)
