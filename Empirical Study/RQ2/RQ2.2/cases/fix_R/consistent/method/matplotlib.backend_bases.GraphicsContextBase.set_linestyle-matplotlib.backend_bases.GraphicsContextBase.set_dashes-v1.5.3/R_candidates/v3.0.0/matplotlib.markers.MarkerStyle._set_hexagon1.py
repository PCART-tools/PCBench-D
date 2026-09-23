    def _set_hexagon1(self):
        self._transform = Affine2D().scale(0.5)
        self._snap_threshold = None

        fs = self.get_fillstyle()
        polypath = Path.unit_regular_polygon(6)

        if not self._half_fill():
            self._path = polypath
        else:
            verts = polypath.vertices

            # not drawing inside lines
            x = np.abs(np.cos(5 * np.pi / 6.))
            top = Path(np.vstack(([-x, 0], verts[(1, 0, 5), :], [x, 0])))
            bottom = Path(np.vstack(([-x, 0], verts[2:5, :], [x, 0])))
            left = Path(verts[(0, 1, 2, 3), :])
            right = Path(verts[(0, 5, 4, 3), :])

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
