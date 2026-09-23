    @staticmethod
    def to_rgba(arg, alpha=None):
        """
        Returns an *RGBA* tuple of four floats from 0-1.

        For acceptable values of *arg*, see :meth:`to_rgb`.
        In addition, if *arg* is "none" (case-insensitive),
        then (0,0,0,0) will be returned.
        If *arg* is an *RGBA* sequence and *alpha* is not *None*,
        *alpha* will replace the original *A*.
        """
        return to_rgba(arg, alpha)
