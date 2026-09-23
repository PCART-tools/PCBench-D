    def __init__(self, xy1, xy2, slope, **kwargs):
        super().__init__([0, 1], [0, 1], **kwargs)

        if (xy2 is None and slope is None or
                xy2 is not None and slope is not None):
            raise TypeError(
                "Exactly one of 'xy2' and 'slope' must be given")

        self._slope = slope
        self._xy1 = xy1
        self._xy2 = xy2
