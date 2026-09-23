    def __init__(self, vertices, codes=None, _interpolation_steps=1,
                 closed=False, readonly=False):
        """
        Create a new path with the given vertices and codes.

        Parameters
        ----------
        vertices : (N, 2) array-like
            The path vertices, as an array, masked array or sequence of pairs.
            Masked values, if any, will be converted to NaNs, which are then
            handled correctly by the Agg PathIterator and other consumers of
            path data, such as :meth:`iter_segments`.
        codes : array-like or None, optional
            N-length array of integers representing the codes of the path.
            If not None, codes must be the same length as vertices.
            If None, *vertices* will be treated as a series of line segments.
        _interpolation_steps : int, optional
            Used as a hint to certain projections, such as Polar, that this
            path should be linearly interpolated immediately before drawing.
            This attribute is primarily an implementation detail and is not
            intended for public use.
        closed : bool, optional
            If *codes* is None and closed is True, vertices will be treated as
            line segments of a closed polygon.  Note that the last vertex will
            then be ignored (as the corresponding code will be set to
            `CLOSEPOLY`).
        readonly : bool, optional
            Makes the path behave in an immutable way and sets the vertices
            and codes as read-only arrays.
        """
        vertices = _to_unmasked_float_array(vertices)
        _api.check_shape((None, 2), vertices=vertices)

        if codes is not None and len(vertices):
            codes = np.asarray(codes, self.code_type)
            if codes.ndim != 1 or len(codes) != len(vertices):
                raise ValueError("'codes' must be a 1D list or array with the "
                                 "same length of 'vertices'. "
                                 f"Your vertices have shape {vertices.shape} "
                                 f"but your codes have shape {codes.shape}")
            if len(codes) and codes[0] != self.MOVETO:
                raise ValueError("The first element of 'code' must be equal "
                                 f"to 'MOVETO' ({self.MOVETO}).  "
                                 f"Your first code is {codes[0]}")
        elif closed and len(vertices):
            codes = np.empty(len(vertices), dtype=self.code_type)
            codes[0] = self.MOVETO
            codes[1:-1] = self.LINETO
            codes[-1] = self.CLOSEPOLY

        self._vertices = vertices
        self._codes = codes
        self._interpolation_steps = _interpolation_steps
        self._update_values()

        if readonly:
            self._vertices.flags.writeable = False
            if self._codes is not None:
                self._codes.flags.writeable = False
            self._readonly = True
        else:
            self._readonly = False
