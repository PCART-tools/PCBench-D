class NullFormatter(Formatter):
    """Always return the empty string."""

    def __call__(self, x, pos=None):
        # docstring inherited
        return ''
