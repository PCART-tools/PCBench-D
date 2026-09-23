    def __init__(self, offset=(2, -2),
                 shadow_color='k', alpha=0.3, rho=0.3, **kwargs):
        """
        Parameters
        ----------
        offset : pair of floats
            The offset to apply to the path, in points.
        shadow_color : color
            The shadow color. Default is black.
            A value of ``None`` takes the original artist's color
            with a scale factor of `rho`.
        alpha : float
            The alpha transparency of the created shadow patch.
            Default is 0.3.
        rho : float
            A scale factor to apply to the rgbFace color if `shadow_rgbFace`
            is ``None``. Default is 0.3.
        **kwargs
            Extra keywords are stored and passed through to
            :meth:`AbstractPathEffect._update_gc`.
        """
        super().__init__(offset)
        if shadow_color is None:
            self._shadow_color = shadow_color
        else:
            self._shadow_color = mcolors.to_rgba(shadow_color)
        self._alpha = alpha
        self._rho = rho
        #: The dictionary of keywords to update the graphics collection with.
        self._gc = kwargs
