    def __init__(self, width, height, xdescent=0.,
                 ydescent=0., clip=False):
        """
        *width*, *height* : width and height of the container box.
        *xdescent*, *ydescent* : descent of the box in x- and y-direction.
        *clip* : Whether to clip the children
        """

        super().__init__()

        self.width = width
        self.height = height
        self.xdescent = xdescent
        self.ydescent = ydescent
        self._clip_children = clip

        self.offset_transform = mtransforms.Affine2D()
        self.offset_transform.clear()
        self.offset_transform.translate(0, 0)

        self.dpi_transform = mtransforms.Affine2D()
