    def __init__(self, offset=(0., 0.)):
        """
        Parameters
        ----------
        offset : pair of floats
            The offset to apply to the path, measured in points.
        """
        self._offset = offset
        self._offset_trans = mtransforms.Affine2D()
