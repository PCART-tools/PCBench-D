    def __sub__(self, rhs):
        """
        Subtract two Epoch's or a Duration from an Epoch.

        Valid:
        Duration = Epoch - Epoch
        Epoch = Epoch - Duration

        = INPUT VARIABLES
        - rhs     The Epoch to subtract.

        = RETURN VALUE
        - Returns either the duration between to Epoch's or the a new
          Epoch that is the result of subtracting a duration from an epoch.
        """
        # Delay-load due to circular dependencies.
        import matplotlib.testing.jpl_units as U

        # Handle Epoch - Duration
        if isinstance(rhs, U.Duration):
            return self + -rhs

        t = self
        if self._frame != rhs._frame:
            t = self.convert(rhs._frame)

        days = t._jd - rhs._jd
        sec = t._seconds - rhs._seconds

        return U.Duration(rhs._frame, days*86400 + sec)
