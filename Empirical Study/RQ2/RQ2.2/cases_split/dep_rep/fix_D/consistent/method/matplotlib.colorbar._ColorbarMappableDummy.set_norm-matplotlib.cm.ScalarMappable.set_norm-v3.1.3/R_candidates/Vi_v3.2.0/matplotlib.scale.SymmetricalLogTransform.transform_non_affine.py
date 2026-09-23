    def transform_non_affine(self, a):
        abs_a = np.abs(a)
        with np.errstate(divide="ignore", invalid="ignore"):
            out = np.sign(a) * self.linthresh * (
                self._linscale_adj +
                np.log(abs_a / self.linthresh) / self._log_base)
            inside = abs_a <= self.linthresh
        out[inside] = a[inside] * self._linscale_adj
        return out
