    def to_pytimedelta(self) -> np.ndarray:
        """
        Return Timedelta Array/Index as object ndarray of datetime.timedelta
        objects.

        Returns
        -------
        timedeltas : ndarray[object]
        """
        return tslibs.ints_to_pytimedelta(self.asi8)
