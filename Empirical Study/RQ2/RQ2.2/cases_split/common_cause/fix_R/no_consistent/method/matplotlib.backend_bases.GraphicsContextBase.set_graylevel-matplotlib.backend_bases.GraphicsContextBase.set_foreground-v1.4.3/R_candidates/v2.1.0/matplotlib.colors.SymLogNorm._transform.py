    def _transform(self, a):
        """
        Inplace transformation.
        """
        masked = np.abs(a) > self.linthresh
        sign = np.sign(a[masked])
        log = (self._linscale_adj + np.log(np.abs(a[masked]) / self.linthresh))
        log *= sign * self.linthresh
        a[masked] = log
        a[~masked] *= self._linscale_adj
        return a
