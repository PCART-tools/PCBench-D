    def range(start, stop, step=None):
        """Generate a range of UnitDbl objects.

        Similar to the Python range() method.  Returns the range [
        start, stop) at the requested step.  Each element will be a
        UnitDbl object.

        = INPUT VARIABLES
        - start     The starting value of the range.
        - stop      The stop value of the range.
        - step      Optional step to use.  If set to None, then a UnitDbl of
                      value 1 w/ the units of the start is used.

        = RETURN VALUE
        - Returns a list containing the requested UnitDbl values.
        """
        if step is None:
            step = UnitDbl(1, start._units)

        elems = []

        i = 0
        while True:
            d = start + i * step
            if d >= stop:
                break

            elems.append(d)
            i += 1

        return elems
