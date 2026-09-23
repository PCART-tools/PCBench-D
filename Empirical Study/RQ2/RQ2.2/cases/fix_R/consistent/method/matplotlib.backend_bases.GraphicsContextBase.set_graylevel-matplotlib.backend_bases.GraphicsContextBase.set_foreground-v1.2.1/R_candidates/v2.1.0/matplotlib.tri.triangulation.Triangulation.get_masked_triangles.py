    def get_masked_triangles(self):
        """
        Return an array of triangles that are not masked.
        """
        if self.mask is not None:
            return self.triangles.compress(1 - self.mask, axis=0)
        else:
            return self.triangles
