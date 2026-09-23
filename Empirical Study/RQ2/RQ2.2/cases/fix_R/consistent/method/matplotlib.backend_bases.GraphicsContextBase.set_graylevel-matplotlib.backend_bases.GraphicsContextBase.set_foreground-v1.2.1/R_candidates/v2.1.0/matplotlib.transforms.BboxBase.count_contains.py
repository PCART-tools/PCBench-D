    def count_contains(self, vertices):
        """
        Count the number of vertices contained in the :class:`Bbox`.
        Any vertices with a non-finite x or y value are ignored.

        *vertices* is a Nx2 Numpy array.
        """
        if len(vertices) == 0:
            return 0
        vertices = np.asarray(vertices)
        with np.errstate(invalid='ignore'):
            return (((self.min < vertices) &
                     (vertices < self.max)).all(axis=1).sum())
