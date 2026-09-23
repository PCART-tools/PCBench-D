    def __init__(self, scale_transform, limits):
        """
        *limits* is the view limit of the data.  The only part of
        its bounds that is used is the y limits (for the radius limits).
        The theta range is handled by the non-affine transform.
        """
        mtransforms.Affine2DBase.__init__(self)
        self._scale_transform = scale_transform
        self._limits = limits
        self.set_children(scale_transform, limits)
        self._mtx = None
