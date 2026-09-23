    def __init__(self, x, y, triangles=None, mask=None):
        from matplotlib import _qhull

        self.x = np.asarray(x, dtype=np.float64)
        self.y = np.asarray(y, dtype=np.float64)
        if self.x.shape != self.y.shape or self.x.ndim != 1:
            raise ValueError("x and y must be equal-length 1D arrays, but "
                             f"found shapes {self.x.shape!r} and "
                             f"{self.y.shape!r}")

        self.mask = None
        self._edges = None
        self._neighbors = None
        self.is_delaunay = False

        if triangles is None:
            # No triangulation specified, so use matplotlib._qhull to obtain
            # Delaunay triangulation.
            self.triangles, self._neighbors = _qhull.delaunay(x, y, sys.flags.verbose)
            self.is_delaunay = True
        else:
            # Triangulation specified. Copy, since we may correct triangle
            # orientation.
            try:
                self.triangles = np.array(triangles, dtype=np.int32, order='C')
            except ValueError as e:
                raise ValueError('triangles must be a (N, 3) int array, not '
                                 f'{triangles!r}') from e
            if self.triangles.ndim != 2 or self.triangles.shape[1] != 3:
                raise ValueError(
                    'triangles must be a (N, 3) int array, but found shape '
                    f'{self.triangles.shape!r}')
            if self.triangles.max() >= len(self.x):
                raise ValueError(
                    'triangles are indices into the points and must be in the '
                    f'range 0 <= i < {len(self.x)} but found value '
                    f'{self.triangles.max()}')
            if self.triangles.min() < 0:
                raise ValueError(
                    'triangles are indices into the points and must be in the '
                    f'range 0 <= i < {len(self.x)} but found value '
                    f'{self.triangles.min()}')

        # Underlying C++ object is not created until first needed.
        self._cpp_triangulation = None

        # Default TriFinder not created until needed.
        self._trifinder = None

        self.set_mask(mask)
