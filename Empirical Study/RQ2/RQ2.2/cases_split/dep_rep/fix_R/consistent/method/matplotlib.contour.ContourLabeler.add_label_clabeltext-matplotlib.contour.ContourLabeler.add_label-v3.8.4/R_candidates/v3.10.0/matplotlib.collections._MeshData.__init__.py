    def __init__(self, coordinates, *, shading='flat'):
        _api.check_shape((None, None, 2), coordinates=coordinates)
        self._coordinates = coordinates
        self._shading = shading
