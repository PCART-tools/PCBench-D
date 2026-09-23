    def _cmp(self, op, rhs):
        """Compare Epochs *self* and *rhs* using operator *op*."""
        t = self
        if self._frame != rhs._frame:
            t = self.convert(rhs._frame)
        if t._jd != rhs._jd:
            return op(t._jd, rhs._jd)
        return op(t._seconds, rhs._seconds)
