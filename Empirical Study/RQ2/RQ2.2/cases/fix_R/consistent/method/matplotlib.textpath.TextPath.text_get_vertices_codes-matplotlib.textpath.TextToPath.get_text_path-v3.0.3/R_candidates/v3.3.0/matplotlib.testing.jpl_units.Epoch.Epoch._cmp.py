    def _cmp(self, rhs, op):
        """
        Compare two Epoch's.

        = INPUT VARIABLES
        - rhs     The Epoch to compare against.
        - op      The function to do the comparison

        = RETURN VALUE
        - Returns op(self, rhs)
        """
        t = self
        if self._frame != rhs._frame:
            t = self.convert(rhs._frame)

        if t._jd != rhs._jd:
            return op(t._jd, rhs._jd)

        return op(t._seconds, rhs._seconds)
