    @docstring.dedent_interpd
    def __init__(self, xy, width, height, angle=0.0, **kwargs):
        """
        *xy*
          center of ellipse

        *width*
          total length (diameter) of horizontal axis

        *height*
          total length (diameter) of vertical axis

        *angle*
          rotation in degrees (anti-clockwise)

        Valid kwargs are:
        %(Patch)s
        """
        Patch.__init__(self, **kwargs)

        self.center = xy
        self.width, self.height = width, height
        self.angle = angle
        self._path = Path.unit_circle()
        # Note: This cannot be calculated until this is added to an Axes
        self._patch_transform = transforms.IdentityTransform()
