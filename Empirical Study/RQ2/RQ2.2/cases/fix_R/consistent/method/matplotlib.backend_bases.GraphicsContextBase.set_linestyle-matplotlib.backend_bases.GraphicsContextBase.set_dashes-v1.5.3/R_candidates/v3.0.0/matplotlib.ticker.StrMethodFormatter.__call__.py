    def __call__(self, x, pos=None):
        """
        Return the formatted label string.

        `x` and `pos` are passed to `str.format` as keyword arguments
        with those exact names.
        """
        return self.fmt.format(x=x, pos=pos)
