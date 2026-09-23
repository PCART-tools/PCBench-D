    def __init__(self, coordinates, *, antialiased=True, shading='flat',
                 **kwargs):
        kwargs.setdefault("pickradius", 0)
        # end of signature deprecation code

        _api.check_shape((None, None, 2), coordinates=coordinates)
        self._coordinates = coordinates
        self._antialiased = antialiased
        self._shading = shading
        self._bbox = transforms.Bbox.unit()
        self._bbox.update_from_data_xy(self._coordinates.reshape(-1, 2))
        # super init delayed after own init because array kwarg requires
        # self._coordinates and self._shading
        super().__init__(**kwargs)
        self.set_mouseover(False)
