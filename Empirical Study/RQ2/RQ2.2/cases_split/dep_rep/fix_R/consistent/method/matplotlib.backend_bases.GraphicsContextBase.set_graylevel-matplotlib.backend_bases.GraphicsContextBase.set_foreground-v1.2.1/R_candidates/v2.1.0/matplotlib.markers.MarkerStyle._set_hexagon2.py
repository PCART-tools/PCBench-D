    def _set_hexagon2(self):
        self._transform = Affine2D().scale(0.5).rotate_deg(30)
        self._snap_threshold = None

        fs = self.get_fillstyle()
        polypath = Path.unit_regular_polygon(6)

        if not self._half_fill():
            self._path = polypath
        else:
            verts = polypath.vertices

            # not drawing inside lines
            x, y = np.sqrt(3) / 4, 3 / 4.
            top = Path(verts[(1, 0, 5, 4, 1), :])
            bottom = Path(verts[(1, 2, 3, 4), :])
            left = Path(np.vstack(([x, y], verts[(0, 1, 2), :],
                                   [-x, -y], [x, y])))
            right = Path(np.vstack(([x, y], verts[(5, 4, 3), :], [-x, -y])))

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
