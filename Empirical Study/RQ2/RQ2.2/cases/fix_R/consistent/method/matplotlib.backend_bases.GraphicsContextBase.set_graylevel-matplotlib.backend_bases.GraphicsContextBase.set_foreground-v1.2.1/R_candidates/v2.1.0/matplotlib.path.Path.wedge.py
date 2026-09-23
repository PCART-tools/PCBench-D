    @classmethod
    def wedge(cls, theta1, theta2, n=None):
        """
        Return a wedge of the unit circle from angle
        *theta1* to angle *theta2* (in degrees).

        *theta2* is unwrapped to produce the shortest wedge within 360 degrees.
        That is, if *theta2* > *theta1* + 360, the wedge will be from *theta1*
        to *theta2* - 360 and not a full circle plus some extra overlap.

        If *n* is provided, it is the number of spline segments to make.
        If *n* is not provided, the number of spline segments is
        determined based on the delta between *theta1* and *theta2*.
        """
        return cls.arc(theta1, theta2, n, True)
