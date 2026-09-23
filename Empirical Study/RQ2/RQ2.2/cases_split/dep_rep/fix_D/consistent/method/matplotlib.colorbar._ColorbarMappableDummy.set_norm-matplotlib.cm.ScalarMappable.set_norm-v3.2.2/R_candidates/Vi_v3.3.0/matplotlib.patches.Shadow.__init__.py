    @cbook._delete_parameter("3.3", "props")
    @docstring.dedent_interpd
    def __init__(self, patch, ox, oy, props=None, **kwargs):
        """
        Create a shadow of the given *patch*.

        By default, the shadow will have the same face color as the *patch*,
        but darkened.

        Parameters
        ----------
        patch : `.Patch`
            The patch to create the shadow for.
        ox, oy : float
            The shift of the shadow in data coordinates, scaled by a factor
            of dpi/72.
        props : dict
            *deprecated (use kwargs instead)* Properties of the shadow patch.
        **kwargs
            Properties of the shadow patch. Supported keys are:

            %(Patch)s
        """
        Patch.__init__(self)
        self.patch = patch
        # Note: when removing props, we can directly pass kwargs to _update()
        # and remove self._props
        if props is None:
            color = .3 * np.asarray(colors.to_rgb(self.patch.get_facecolor()))
            props = {
                'facecolor': color,
                'edgecolor': color,
                'alpha': 0.5,
            }
        self._props = {**props, **kwargs}
        self._ox, self._oy = ox, oy
        self._shadow_transform = transforms.Affine2D()
        self._update()
