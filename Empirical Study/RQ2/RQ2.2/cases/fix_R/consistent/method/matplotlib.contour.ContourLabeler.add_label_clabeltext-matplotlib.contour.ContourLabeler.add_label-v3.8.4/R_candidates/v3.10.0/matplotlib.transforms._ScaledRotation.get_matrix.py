    def get_matrix(self):
        if self._invalid:
            transformed_coords = self._trans_shift.transform([[self._theta, 0]])[0]
            adjusted_theta = transformed_coords[0]
            rotation = Affine2D().rotate(adjusted_theta)
            self._mtx = rotation.get_matrix()
        return self._mtx
