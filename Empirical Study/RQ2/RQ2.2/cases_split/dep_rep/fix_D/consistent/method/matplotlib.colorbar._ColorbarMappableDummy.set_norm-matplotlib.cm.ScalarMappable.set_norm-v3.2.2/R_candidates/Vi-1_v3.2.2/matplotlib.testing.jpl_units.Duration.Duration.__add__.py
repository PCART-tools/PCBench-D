    def __add__(self, rhs):
        """Add two Durations.

        = ERROR CONDITIONS
        - If the input rhs is not in the same frame, an error is thrown.

        = INPUT VARIABLES
        - rhs     The Duration to add.

        = RETURN VALUE
        - Returns the sum of ourselves and the input Duration.
        """
        # Delay-load due to circular dependencies.
        import matplotlib.testing.jpl_units as U

        if isinstance(rhs, U.Epoch):
            return rhs + self

        self.checkSameFrame(rhs, "add")
        return Duration(self._frame, self._seconds + rhs._seconds)
