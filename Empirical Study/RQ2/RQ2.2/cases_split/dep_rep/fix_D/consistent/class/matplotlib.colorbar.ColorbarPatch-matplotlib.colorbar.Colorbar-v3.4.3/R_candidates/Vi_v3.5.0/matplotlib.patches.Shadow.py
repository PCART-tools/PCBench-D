class Shadow(Patch):
    def __str__(self):
        return "Shadow(%s)" % (str(self.patch))

    @docstring.dedent_interpd
    def __init__(self, patch, ox, oy, **kwargs):
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
        **kwargs
            Properties of the shadow patch. Supported keys are:

            %(Patch:kwdoc)s
        """
        super().__init__()
        self.patch = patch
        self._ox, self._oy = ox, oy
        self._shadow_transform = transforms.Affine2D()

        self.update_from(self.patch)
        color = .3 * np.asarray(colors.to_rgb(self.patch.get_facecolor()))
        self.update({'facecolor': color, 'edgecolor': color, 'alpha': 0.5,
                     # Place shadow patch directly behind the inherited patch.
                     'zorder': np.nextafter(self.patch.zorder, -np.inf),
                     **kwargs})

    def _update_transform(self, renderer):
        ox = renderer.points_to_pixels(self._ox)
        oy = renderer.points_to_pixels(self._oy)
        self._shadow_transform.clear().translate(ox, oy)

    def get_path(self):
        return self.patch.get_path()

    def get_patch_transform(self):
        return self.patch.get_patch_transform() + self._shadow_transform

    def draw(self, renderer):
        self._update_transform(renderer)
        super().draw(renderer)
