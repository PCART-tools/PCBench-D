    def __init__(self, *args, **kwargs):
        # signature deprecation since="3.5": Change to new signature after the
        # deprecation has expired. Also remove setting __init__.__signature__,
        # and remove the Notes from the docstring.
        params = _api.select_matching_signature(
            [
                lambda meshWidth, meshHeight, coordinates, antialiased=True,
                       shading='flat', **kwargs: locals(),
                lambda coordinates, antialiased=True, shading='flat', **kwargs:
                       locals()
            ],
            *args, **kwargs).values()
        *old_w_h, coords, antialiased, shading, kwargs = params
        if old_w_h:  # The old signature matched.
            _api.warn_deprecated(
                "3.5",
                message="This usage of Quadmesh is deprecated: Parameters "
                        "meshWidth and meshHeights will be removed; "
                        "coordinates must be 2D; all parameters except "
                        "coordinates will be keyword-only.")
            w, h = old_w_h
            coords = np.asarray(coords, np.float64).reshape((h + 1, w + 1, 2))
        kwargs.setdefault("pickradius", 0)
        # end of signature deprecation code

        _api.check_shape((None, None, 2), coordinates=coords)
        self._coordinates = coords
        self._antialiased = antialiased
        self._shading = shading
        self._bbox = transforms.Bbox.unit()
        self._bbox.update_from_data_xy(self._coordinates.reshape(-1, 2))
        # super init delayed after own init because array kwarg requires
        # self._coordinates and self._shading
        super().__init__(**kwargs)
