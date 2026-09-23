    def _set_custom_marker(self, path):
        verts = path.vertices
        rescale = max(np.max(np.abs(verts[:, 0])),
                      np.max(np.abs(verts[:, 1])))
        self._transform = Affine2D().scale(0.5 / rescale)
        self._path = path
