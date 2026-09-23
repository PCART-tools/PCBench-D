    def frozen(self):
        # docstring inherited
        return Affine2D(self.get_matrix().copy())
