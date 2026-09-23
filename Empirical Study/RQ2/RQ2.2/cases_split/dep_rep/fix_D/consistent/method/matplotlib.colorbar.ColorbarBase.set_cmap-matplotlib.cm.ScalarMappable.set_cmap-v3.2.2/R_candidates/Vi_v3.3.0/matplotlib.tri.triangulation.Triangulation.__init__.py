    def __init__(self, x, y, triangles=None, mask=None):
        from matplotlib import _qhull

        self.x = np.asarray(x, dtype=np.float64)
        self.y = np.asarray(y, dtype=np.float64)
        if self.x.shape != self.y.shape or self.x.ndim != 1:
            raise ValueError("x and y must be equal-length 1-D arrays")

        self.mask = None
        self._edges = None
        self._neighbors = None
        self.is_delaunay = False

        if triangles is None:
            # No triangulation specified, so use matplotlib._qhull to obtain
            # Delaunay triangulation.
            self.triangles, self._neighbors = _qhull.delaunay(x, y)
            self.is_delaunay = True
        else:
            # Triangulation specified. Copy, since we may correct triangle
            # orientation.
            self.triangles = np.array(triangles, dtype=np.int32, order='C')
            if self.triangles.ndim != 2 or self.triangles.shape[1] != 3:
                raise ValueError('triangles must be a (?, 3) array')
            if self.triangles.max() >= len(self.x):
                raise ValueError('triangles max element is out of bounds')
            if self.triangles.min() < 0:
                raise ValueError('triangles min element is out of bounds')

        if mask is not None:
            self.mask = np.asarray(mask, dtype=bool)
            if self.mask.shape != (self.triangles.shape[0],):
                raise ValueError('mask array must have same length as '
                                 'triangles array')

        # Underlying C++ object is not created until first needed.
        self._cpp_triangulation = None

        # Default TriFinder not created until needed.
        self._trifinder = None
