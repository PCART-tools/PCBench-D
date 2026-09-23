    def __init__(self, *args, **kwargs):
        self._longitude_cap = np.pi / 2.0
        self._center_longitude = kwargs.pop("center_longitude", 0.0)
        self._center_latitude = kwargs.pop("center_latitude", 0.0)
        GeoAxes.__init__(self, *args, **kwargs)
        self.set_aspect('equal', adjustable='box', anchor='C')
        self.cla()
