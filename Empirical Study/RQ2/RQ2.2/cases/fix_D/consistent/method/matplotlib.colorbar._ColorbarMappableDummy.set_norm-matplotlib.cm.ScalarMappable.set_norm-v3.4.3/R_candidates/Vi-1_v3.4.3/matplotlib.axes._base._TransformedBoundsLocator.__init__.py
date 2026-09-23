    def __init__(self, bounds, transform):
        """
        *bounds* (a ``[l, b, w, h]`` rectangle) and *transform* together
        specify the position of the inset axes.
        """
        self._bounds = bounds
        self._transform = transform
