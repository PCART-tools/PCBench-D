    @property
    def _combined(self) -> IntervalSideT:
        left = self.left._values.reshape(-1, 1)
        right = self.right._values.reshape(-1, 1)
        if needs_i8_conversion(left.dtype):
            comb = left._concat_same_type([left, right], axis=1)
        else:
            comb = np.concatenate([left, right], axis=1)
        return comb
