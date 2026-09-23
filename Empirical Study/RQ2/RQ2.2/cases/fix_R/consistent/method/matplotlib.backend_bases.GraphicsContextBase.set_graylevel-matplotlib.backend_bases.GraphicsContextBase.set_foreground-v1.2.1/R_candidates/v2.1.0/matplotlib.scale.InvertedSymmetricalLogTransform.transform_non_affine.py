    def transform_non_affine(self, a):
        sign = np.sign(a)
        masked = ma.masked_inside(a, -self.invlinthresh,
                                  self.invlinthresh, copy=False)
        exp = sign * self.linthresh * (
            ma.power(self.base, (sign * (masked / self.linthresh))
            - self._linscale_adj))
        if masked.mask.any():
            return ma.where(masked.mask, a / self._linscale_adj, exp)
        else:
            return exp
