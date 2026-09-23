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
        alpha : float, default: 0.3
            The alpha transparency of the created shadow patch.
            http://matplotlib.1069221.n5.nabble.com/path-effects-question-td27630.html
        rho : float, default: 0.3
            A scale factor to apply to the rgbFace color if `shadow_rgbFace`
            is not specified.
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
