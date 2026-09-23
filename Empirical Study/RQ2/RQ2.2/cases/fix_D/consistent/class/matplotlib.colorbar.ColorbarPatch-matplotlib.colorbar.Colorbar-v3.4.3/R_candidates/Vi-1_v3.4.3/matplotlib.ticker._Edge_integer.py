class _Edge_integer:
    """
    Helper for MaxNLocator, MultipleLocator, etc.

    Take floating point precision limitations into account when calculating
    tick locations as integer multiples of a step.
    """
    def __init__(self, step, offset):
        """
        *step* is a positive floating-point interval between ticks.
        *offset* is the offset subtracted from the data limits
        prior to calculating tick locations.
        """
        if step <= 0:
            raise ValueError("'step' must be positive")
        self.step = step
        self._offset = abs(offset)

    def closeto(self, ms, edge):
        # Allow more slop when the offset is large compared to the step.
        if self._offset > 0:
            digits = np.log10(self._offset / self.step)
            tol = max(1e-10, 10 ** (digits - 12))
            tol = min(0.4999, tol)
        else:
            tol = 1e-10
        return abs(ms - edge) < tol

    def le(self, x):
        """Return the largest n: n*step <= x."""
        d, m = divmod(x, self.step)
        if self.closeto(m / self.step, 1):
            return d + 1
        return d

    def ge(self, x):
        """Return the smallest n: n*step >= x."""
        d, m = divmod(x, self.step)
        if self.closeto(m / self.step, 0):
            return d
        return d + 1
