    def _set_hexagon1(self):
        self._transform = Affine2D().scale(0.5)
        self._snap_threshold = None

        polypath = Path.unit_regular_polygon(6)

        if not self._half_fill():
            self._path = polypath
        else:
            verts = polypath.vertices
            # not drawing inside lines
            x = np.abs(np.cos(5 * np.pi / 6.))
            top = Path(np.concatenate([[(-x, 0)], verts[[1, 0, 5]], [(x, 0)]]))
            bottom = Path(np.concatenate([[(-x, 0)], verts[2:5], [(x, 0)]]))
            left = Path(verts[0:4])
            right = Path(verts[[0, 5, 4, 3]])
            self._path, self._alt_path = {
                'top': (top, bottom), 'bottom': (bottom, top),
                'left': (left, right), 'right': (right, left),
            }[self.get_fillstyle()]
            self._alt_transform = self._transform

        self._joinstyle = self._user_joinstyle or JoinStyle.miter
