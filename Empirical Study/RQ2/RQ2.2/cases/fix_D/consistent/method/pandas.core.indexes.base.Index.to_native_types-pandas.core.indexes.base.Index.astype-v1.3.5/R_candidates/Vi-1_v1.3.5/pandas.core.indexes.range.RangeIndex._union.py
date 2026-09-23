    def _union(self, other: Index, sort):
        """
        Form the union of two Index objects and sorts if possible

        Parameters
        ----------
        other : Index or array-like

        sort : False or None, default None
            Whether to sort resulting index. ``sort=None`` returns a
            monotonically increasing ``RangeIndex`` if possible or a sorted
            ``Int64Index`` if not. ``sort=False`` always returns an
            unsorted ``Int64Index``

            .. versionadded:: 0.25.0

        Returns
        -------
        union : Index
        """
        if isinstance(other, RangeIndex) and sort is None:
            start_s, step_s = self.start, self.step
            end_s = self.start + self.step * (len(self) - 1)
            start_o, step_o = other.start, other.step
            end_o = other.start + other.step * (len(other) - 1)
            if self.step < 0:
                start_s, step_s, end_s = end_s, -step_s, start_s
            if other.step < 0:
                start_o, step_o, end_o = end_o, -step_o, start_o
            if len(self) == 1 and len(other) == 1:
                step_s = step_o = abs(self.start - other.start)
            elif len(self) == 1:
                step_s = step_o
            elif len(other) == 1:
                step_o = step_s
            start_r = min(start_s, start_o)
            end_r = max(end_s, end_o)
            if step_o == step_s:
                if (
                    (start_s - start_o) % step_s == 0
                    and (start_s - end_o) <= step_s
                    and (start_o - end_s) <= step_s
                ):
                    return type(self)(start_r, end_r + step_s, step_s)
                if (
                    (step_s % 2 == 0)
                    and (abs(start_s - start_o) <= step_s / 2)
                    and (abs(end_s - end_o) <= step_s / 2)
                ):
                    return type(self)(start_r, end_r + step_s / 2, step_s / 2)
            elif step_o % step_s == 0:
                if (
                    (start_o - start_s) % step_s == 0
                    and (start_o + step_s >= start_s)
                    and (end_o - step_s <= end_s)
                ):
                    return type(self)(start_r, end_r + step_s, step_s)
            elif step_s % step_o == 0:
                if (
                    (start_s - start_o) % step_o == 0
                    and (start_s + step_o >= start_o)
                    and (end_s - step_o <= end_o)
                ):
                    return type(self)(start_r, end_r + step_o, step_o)
        return self._int64index._union(other, sort=sort)
