    def frozen(self):
        return Affine2D(self.get_matrix().copy())
