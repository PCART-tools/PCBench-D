    def __call__(self, x, pos=None):
        """
        Return the category label string for tick val *x*.

        The position *pos* is ignored.
        """
        return self.format_ticks([x])[0]
