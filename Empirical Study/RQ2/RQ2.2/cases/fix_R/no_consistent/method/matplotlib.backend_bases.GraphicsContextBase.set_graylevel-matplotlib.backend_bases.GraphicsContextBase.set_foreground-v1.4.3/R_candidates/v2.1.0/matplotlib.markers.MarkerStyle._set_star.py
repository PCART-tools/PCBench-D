    def _set_star(self):
        self._transform = Affine2D().scale(0.5)
        self._snap_threshold = 5.0

        fs = self.get_fillstyle()
        polypath = Path.unit_regular_star(5, innerCircle=0.381966)

        if not self._half_fill():
            self._path = polypath
        else:
            verts = polypath.vertices

            top = Path(np.vstack((verts[0:4, :], verts[7:10, :], verts[0])))
            bottom = Path(np.vstack((verts[3:8, :], verts[3])))
            left = Path(np.vstack((verts[0:6, :], verts[0])))
            right = Path(np.vstack((verts[0], verts[5:10, :], verts[0])))

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

        self._joinstyle = 'bevel'
