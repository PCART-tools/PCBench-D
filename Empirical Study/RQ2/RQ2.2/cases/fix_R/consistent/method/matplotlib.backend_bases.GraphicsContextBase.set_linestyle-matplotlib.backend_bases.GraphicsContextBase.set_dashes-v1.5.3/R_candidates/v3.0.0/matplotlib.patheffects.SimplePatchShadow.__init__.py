    def __init__(self, offset=(2, -2),
                 shadow_rgbFace=None, alpha=None,
                 rho=0.3, **kwargs):
        """
        Parameters
        ----------
        offset : pair of floats
            The offset of the shadow in points.
        shadow_rgbFace : color
            The shadow color.
        alpha : float
            The alpha transparency of the created shadow patch.
            Default is 0.3.
            http://matplotlib.1069221.n5.nabble.com/path-effects-question-td27630.html
        rho : float
            A scale factor to apply to the rgbFace color if `shadow_rgbFace`
            is not specified. Default is 0.3.
        **kwargs
            Extra keywords are stored and passed through to
            :meth:`AbstractPathEffect._update_gc`.

        """
        super().__init__(offset)

        if shadow_rgbFace is None:
            self._shadow_rgbFace = shadow_rgbFace
        else:
            self._shadow_rgbFace = mcolors.to_rgba(shadow_rgbFace)

        if alpha is None:
            alpha = 0.3

        self._alpha = alpha
        self._rho = rho

        #: The dictionary of keywords to update the graphics collection with.
        self._gc = kwargs

        #: The offset transform object. The offset isn't calculated yet
        #: as we don't know how big the figure will be in pixels.
        self._offset_tran = mtransforms.Affine2D()
