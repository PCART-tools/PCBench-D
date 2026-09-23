        def __init__(self, center_longitude, center_latitude, resolution):
            _GeoTransform.__init__(self, resolution)
            self._center_longitude = center_longitude
            self._center_latitude = center_latitude
