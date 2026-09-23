    @staticmethod
    def is_numlike(x):
        """
        The matplotlib datalim, autoscaling, locators etc work with
        scalars which are the units converted to floats given the
        current unit.  The converter may be passed these floats, or
        arrays of them, even when units are set.  Derived conversion
        interfaces may opt to pass plain-ol unitless numbers through
        the conversion interface and this is a helper function for
        them.
        """
        if iterable(x):
            for thisx in x:
                return is_numlike(thisx)
        else:
            return is_numlike(x)
