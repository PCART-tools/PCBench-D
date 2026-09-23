    @classmethod
    def make_compound_path_from_polys(cls, XY):
        """
        Make a compound path object to draw a number
        of polygons with equal numbers of sides XY is a (numpolys x
        numsides x 2) numpy array of vertices.  Return object is a
        :class:`Path`

        .. plot:: gallery/misc/histogram_path.py

        """

        # for each poly: 1 for the MOVETO, (numsides-1) for the LINETO, 1 for
        # the CLOSEPOLY; the vert for the closepoly is ignored but we still
        # need it to keep the codes aligned with the vertices
        numpolys, numsides, two = XY.shape
        if two != 2:
            raise ValueError("The third dimension of 'XY' must be 2")
        stride = numsides + 1
        nverts = numpolys * stride
        verts = np.zeros((nverts, 2))
        codes = np.full(nverts, cls.LINETO, dtype=cls.code_type)
        codes[0::stride] = cls.MOVETO
        codes[numsides::stride] = cls.CLOSEPOLY
        for i in range(numsides):
            verts[i::stride] = XY[:, i]

        return cls(verts, codes)
