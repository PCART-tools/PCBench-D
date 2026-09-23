    @staticmethod
    def is_numlike(x):
        """
        The Matplotlib datalim, autoscaling, locators etc work with
        scalars which are the units converted to floats given the
        current unit.  The converter may be passed these floats, or
        arrays of them, even when units are set.
        """
        if iterable(x):
            for thisx in x:
                return isinstance(thisx, Number)
        else:
            return isinstance(x, Number)
