    @docstring.dedent_interpd
    def __init__(self, verts, sizes=None, closed=True, **kwargs):
        """
        *verts* is a sequence of ( *verts0*, *verts1*, ...) where
        *verts_i* is a sequence of *xy* tuples of vertices, or an
        equivalent :mod:`numpy` array of shape (*nv*, 2).

        *sizes* is *None* (default) or a sequence of floats that
        scale the corresponding *verts_i*.  The scaling is applied
        before the Artist master transform; if the latter is an identity
        transform, then the overall scaling is such that if
        *verts_i* specify a unit square, then *sizes_i* is the area
        of that square in points^2.
        If len(*sizes*) < *nv*, the additional values will be
        taken cyclically from the array.

        *closed*, when *True*, will explicitly close the polygon.

        %(Collection)s
        """
        Collection.__init__(self, **kwargs)
        self.set_sizes(sizes)
        self.set_verts(verts, closed)
        self.stale = True
