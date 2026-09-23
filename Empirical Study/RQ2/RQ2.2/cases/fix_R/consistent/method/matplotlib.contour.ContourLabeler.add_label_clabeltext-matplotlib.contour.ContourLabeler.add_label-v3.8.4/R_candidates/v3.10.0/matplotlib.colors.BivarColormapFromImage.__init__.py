    def __init__(self, lut, shape='square', origin=(0, 0), name='from image'):
        # We can allow for a PIL.Image as input in the following way, but importing
        # matplotlib.image.pil_to_array() results in a circular import
        # For now, this function only accepts numpy arrays.
        # i.e.:
        # if isinstance(Image, lut):
        #    lut = image.pil_to_array(lut)
        lut = np.array(lut, copy=True)
        if lut.ndim != 3 or lut.shape[2] not in (3, 4):
            raise ValueError("The lut must be an array of shape (n, m, 3) or (n, m, 4)",
                             " or a PIL.image encoded as RGB or RGBA")

        if lut.dtype == np.uint8:
            lut = lut.astype(np.float32)/255
        if lut.shape[2] == 3:
            new_lut = np.empty((lut.shape[0], lut.shape[1], 4), dtype=lut.dtype)
            new_lut[:, :, :3] = lut
            new_lut[:, :, 3] = 1.
            lut = new_lut
        self._lut = lut
        super().__init__(lut.shape[0], lut.shape[1], shape, origin, name=name)
