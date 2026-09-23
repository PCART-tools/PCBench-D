    def _set_custom_marker(self, path):
        rescale = np.max(np.abs(path.vertices))  # max of x's and y's.
        self._transform = Affine2D().scale(0.5 / rescale)
        self._path = path
