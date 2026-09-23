    def set_alpha(self, alpha):
        """
        Set the alpha blending value for all ContourSet artists.
        *alpha* must be between 0 (transparent) and 1 (opaque).
        """
        self.alpha = alpha
        self.changed()
