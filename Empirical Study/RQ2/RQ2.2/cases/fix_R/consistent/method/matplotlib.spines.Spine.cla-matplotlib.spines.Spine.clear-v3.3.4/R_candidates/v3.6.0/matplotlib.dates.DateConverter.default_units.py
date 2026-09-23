    @staticmethod
    def default_units(x, axis):
        """
        Return the tzinfo instance of *x* or of its first element, or None
        """
        if isinstance(x, np.ndarray):
            x = x.ravel()

        try:
            x = cbook._safe_first_non_none(x)
        except (TypeError, StopIteration):
            pass

        try:
            return x.tzinfo
        except AttributeError:
            pass
        return None
