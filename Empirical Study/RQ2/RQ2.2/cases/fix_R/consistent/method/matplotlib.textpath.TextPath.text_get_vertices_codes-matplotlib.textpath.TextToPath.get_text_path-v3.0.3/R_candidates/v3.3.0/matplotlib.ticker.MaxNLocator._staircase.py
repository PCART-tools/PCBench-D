    @staticmethod
    def _staircase(steps):
        # Make an extended staircase within which the needed
        # step will be found.  This is probably much larger
        # than necessary.
        flights = (0.1 * steps[:-1], steps, 10 * steps[1])
        return np.hstack(flights)
