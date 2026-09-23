    def __init__(self, child, pad=None, draw_frame=False, patch_attrs=None):
        """
        *pad* : boundary pad

        .. note::
          *pad* need to given in points and will be
          scale with the renderer dpi, while *width* and *height*
          need to be in pixels.
        """

        super(PaddedBox, self).__init__()

        self.pad = pad
        self._children = [child]

        self.patch = FancyBboxPatch(
            xy=(0.0, 0.0), width=1., height=1.,
            facecolor='w', edgecolor='k',
            mutation_scale=1,  # self.prop.get_size_in_points(),
            snap=True
            )

        self.patch.set_boxstyle("square", pad=0)

        if patch_attrs is not None:
            self.patch.update(patch_attrs)

        self._drawFrame = draw_frame
