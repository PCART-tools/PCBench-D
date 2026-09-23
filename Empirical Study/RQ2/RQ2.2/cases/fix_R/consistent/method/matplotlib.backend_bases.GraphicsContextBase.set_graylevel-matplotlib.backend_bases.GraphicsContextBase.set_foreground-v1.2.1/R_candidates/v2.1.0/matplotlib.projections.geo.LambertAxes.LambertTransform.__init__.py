        def __init__(self, center_longitude, center_latitude, resolution):
            """
            Create a new Lambert transform.  Resolution is the number of steps
            to interpolate between each input line segment to approximate its
            path in curved Lambert space.
            """
            Transform.__init__(self)
            self._resolution = resolution
            self._center_longitude = center_longitude
            self._center_latitude = center_latitude
