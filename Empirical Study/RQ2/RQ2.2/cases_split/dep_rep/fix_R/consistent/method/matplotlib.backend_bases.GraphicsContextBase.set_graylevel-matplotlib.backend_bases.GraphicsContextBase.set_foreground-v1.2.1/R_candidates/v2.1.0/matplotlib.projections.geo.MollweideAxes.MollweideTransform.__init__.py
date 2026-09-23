        def __init__(self, resolution):
            """
            Create a new Mollweide transform.  Resolution is the number of steps
            to interpolate between each input line segment to approximate its
            path in curved Mollweide space.
            """
            Transform.__init__(self)
            self._resolution = resolution
