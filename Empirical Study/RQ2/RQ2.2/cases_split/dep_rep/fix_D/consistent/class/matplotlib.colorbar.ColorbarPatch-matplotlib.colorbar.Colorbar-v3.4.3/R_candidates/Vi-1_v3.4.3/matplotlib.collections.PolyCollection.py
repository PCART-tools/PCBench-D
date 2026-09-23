class PolyCollection(_CollectionWithSizes):
    def __init__(self, verts, sizes=None, closed=True, **kwargs):
        """
        Parameters
        ----------
        verts : list of array-like
            The sequence of polygons [*verts0*, *verts1*, ...] where each
            element *verts_i* defines the vertices of polygon *i* as a 2D
            array-like of shape (M, 2).
        sizes : array-like, default: None
            Squared scaling factors for the polygons. The coordinates of each
            polygon *verts_i* are multiplied by the square-root of the
            corresponding entry in *sizes* (i.e., *sizes* specify the scaling
            of areas). The scaling is applied before the Artist master
            transform.
        closed : bool, default: True
            Whether the polygon should be closed by adding a CLOSEPOLY
            connection at the end.
        **kwargs
            Forwarded to `.Collection`.
        """
        super().__init__(**kwargs)
        self.set_sizes(sizes)
        self.set_verts(verts, closed)
        self.stale = True

    def set_verts(self, verts, closed=True):
        """
        Set the vertices of the polygons.

        Parameters
        ----------
        verts : list of array-like
            The sequence of polygons [*verts0*, *verts1*, ...] where each
            element *verts_i* defines the vertices of polygon *i* as a 2D
            array-like of shape (M, 2).
        closed : bool, default: True
            Whether the polygon should be closed by adding a CLOSEPOLY
            connection at the end.
        """
        self.stale = True
        if isinstance(verts, np.ma.MaskedArray):
            verts = verts.astype(float).filled(np.nan)

        # No need to do anything fancy if the path isn't closed.
        if not closed:
            self._paths = [mpath.Path(xy) for xy in verts]
            return

        # Fast path for arrays
        if isinstance(verts, np.ndarray) and len(verts.shape) == 3:
            verts_pad = np.concatenate((verts, verts[:, :1]), axis=1)
            # Creating the codes once is much faster than having Path do it
            # separately each time by passing closed=True.
            codes = np.empty(verts_pad.shape[1], dtype=mpath.Path.code_type)
            codes[:] = mpath.Path.LINETO
            codes[0] = mpath.Path.MOVETO
            codes[-1] = mpath.Path.CLOSEPOLY
            self._paths = [mpath.Path(xy, codes) for xy in verts_pad]
            return

        self._paths = []
        for xy in verts:
            if len(xy):
                if isinstance(xy, np.ma.MaskedArray):
                    xy = np.ma.concatenate([xy, xy[:1]])
                else:
                    xy = np.concatenate([xy, xy[:1]])
                self._paths.append(mpath.Path(xy, closed=True))
            else:
                self._paths.append(mpath.Path(xy))

    set_paths = set_verts

    def set_verts_and_codes(self, verts, codes):
        """Initialize vertices with path codes."""
        if len(verts) != len(codes):
            raise ValueError("'codes' must be a 1D list or array "
                             "with the same length of 'verts'")
        self._paths = []
        for xy, cds in zip(verts, codes):
            if len(xy):
                self._paths.append(mpath.Path(xy, cds))
            else:
                self._paths.append(mpath.Path(xy))
        self.stale = True
