    def __init__(self, meshWidth, meshHeight, coordinates,
                 antialiased=True, shading='flat', **kwargs):
        super().__init__(**kwargs)
        self._meshWidth = meshWidth
        self._meshHeight = meshHeight
        # By converting to floats now, we can avoid that on every draw.
        self._coordinates = np.asarray(coordinates, float).reshape(
            (meshHeight + 1, meshWidth + 1, 2))
        self._antialiased = antialiased
        self._shading = shading

        self._bbox = transforms.Bbox.unit()
        self._bbox.update_from_data_xy(coordinates.reshape(
            ((meshWidth + 1) * (meshHeight + 1), 2)))
