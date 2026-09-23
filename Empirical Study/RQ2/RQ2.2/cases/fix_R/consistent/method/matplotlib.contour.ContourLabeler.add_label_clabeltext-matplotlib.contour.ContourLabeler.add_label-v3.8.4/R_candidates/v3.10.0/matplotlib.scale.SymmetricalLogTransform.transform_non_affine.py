    def transform_non_affine(self, values):
        abs_a = np.abs(values)
        with np.errstate(divide="ignore", invalid="ignore"):
            out = np.sign(values) * self.linthresh * (
                self._linscale_adj +
                np.log(abs_a / self.linthresh) / self._log_base)
            inside = abs_a <= self.linthresh
        out[inside] = values[inside] * self._linscale_adj
        return out
