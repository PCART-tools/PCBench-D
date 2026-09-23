    @docstring.dedent_interpd
    def __init__(self, patch, ox, oy, props=None, **kwargs):
        """
        Create a shadow of the given *patch* offset by *ox*, *oy*.
        *props*, if not *None*, is a patch property update dictionary.
        If *None*, the shadow will have have the same color as the face,
        but darkened.

        Valid keyword arguments are:

        %(Patch)s
        """
        Patch.__init__(self)
        self.patch = patch
        self.props = props
        self._ox, self._oy = ox, oy
        self._shadow_transform = transforms.Affine2D()
        self._update()
