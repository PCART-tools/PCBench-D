    def _iter_break_from_left_to_right(self):
        for lh_compliment, rh_compliment in self._a._iter_break_from_left_to_right():
            yield lh_compliment, rh_compliment + self._b
        for lh_compliment, rh_compliment in self._b._iter_break_from_left_to_right():
            yield self._a + lh_compliment, rh_compliment
