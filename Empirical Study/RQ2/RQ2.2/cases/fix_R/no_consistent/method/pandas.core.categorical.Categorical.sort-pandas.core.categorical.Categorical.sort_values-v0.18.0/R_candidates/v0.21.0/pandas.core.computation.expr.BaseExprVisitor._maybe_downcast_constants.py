    def _maybe_downcast_constants(self, left, right):
        f32 = np.dtype(np.float32)
        if left.isscalar and not right.isscalar and right.return_type == f32:
            # right is a float32 array, left is a scalar
            name = self.env.add_tmp(np.float32(left.value))
            left = self.term_type(name, self.env)
        if right.isscalar and not left.isscalar and left.return_type == f32:
            # left is a float32 array, right is a scalar
            name = self.env.add_tmp(np.float32(right.value))
            right = self.term_type(name, self.env)

        return left, right
