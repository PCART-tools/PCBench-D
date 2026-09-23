    @docstring.dedent_interpd
    def __init__(self, xy, numVertices, radius=5, orientation=0,
                 **kwargs):
        """
        Constructor arguments:

        *xy*
          A length 2 tuple (*x*, *y*) of the center.

        *numVertices*
          the number of vertices.

        *radius*
          The distance from the center to each of the vertices.

        *orientation*
          rotates the polygon (in radians).

        Valid keyword arguments are:

        %(Patch)s
        """
        self._xy = xy
        self._numVertices = numVertices
        self._orientation = orientation
        self._radius = radius
        self._path = Path.unit_regular_polygon(numVertices)
        self._poly_transform = transforms.Affine2D()
        self._update_transform()

        Patch.__init__(self, **kwargs)
