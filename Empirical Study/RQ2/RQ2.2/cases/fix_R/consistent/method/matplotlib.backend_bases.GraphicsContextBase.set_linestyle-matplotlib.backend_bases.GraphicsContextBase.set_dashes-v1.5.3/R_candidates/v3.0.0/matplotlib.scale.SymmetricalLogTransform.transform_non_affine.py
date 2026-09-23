    def transform_non_affine(self, a):
        sign = np.sign(a)
        masked = ma.masked_inside(a,
                                  -self.linthresh,
                                  self.linthresh,
                                  copy=False)
        log = sign * self.linthresh * (
            self._linscale_adj +
            ma.log(np.abs(masked) / self.linthresh) / self._log_base)
        if masked.mask.any():
            return ma.where(masked.mask, a * self._linscale_adj, log)
        else:
            return log
