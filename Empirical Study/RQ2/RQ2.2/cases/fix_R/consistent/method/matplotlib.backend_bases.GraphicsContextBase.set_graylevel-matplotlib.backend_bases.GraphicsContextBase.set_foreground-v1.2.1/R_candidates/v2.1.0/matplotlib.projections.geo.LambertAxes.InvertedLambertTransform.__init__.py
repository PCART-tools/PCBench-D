        def __init__(self, center_longitude, center_latitude, resolution):
            Transform.__init__(self)
            self._resolution = resolution
            self._center_longitude = center_longitude
            self._center_latitude = center_latitude
