    def _set_pentagon(self):
        self._transform = Affine2D().scale(0.5)
        self._snap_threshold = 5.0

        polypath = Path.unit_regular_polygon(5)
        fs = self.get_fillstyle()

        if not self._half_fill():
            self._path = polypath
        else:
            verts = polypath.vertices

            y = (1 + np.sqrt(5)) / 4.
            top = Path([verts[0], verts[1], verts[4], verts[0]])
            bottom = Path([verts[1], verts[2], verts[3], verts[4], verts[1]])
            left = Path([verts[0], verts[1], verts[2], [0, -y], verts[0]])
            right = Path([verts[0], verts[4], verts[3], [0, -y], verts[0]])

            if fs == 'top':
                mpath, mpath_alt = top, bottom
            elif fs == 'bottom':
                mpath, mpath_alt = bottom, top
            elif fs == 'left':
                mpath, mpath_alt = left, right
            else:
                mpath, mpath_alt = right, left
            self._path = mpath
            self._alt_path = mpath_alt
            self._alt_transform = self._transform

        self._joinstyle = 'miter'
