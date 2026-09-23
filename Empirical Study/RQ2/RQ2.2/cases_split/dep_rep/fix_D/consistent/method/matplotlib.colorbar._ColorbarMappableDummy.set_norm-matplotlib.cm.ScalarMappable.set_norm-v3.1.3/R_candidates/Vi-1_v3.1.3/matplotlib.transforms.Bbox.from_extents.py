    @staticmethod
    def from_extents(*args):
        """
        (staticmethod) Create a new Bbox from *left*, *bottom*,
        *right* and *top*.

        The *y*-axis increases upwards.
        """
        points = np.array(args, dtype=float).reshape(2, 2)
        return Bbox(points)
