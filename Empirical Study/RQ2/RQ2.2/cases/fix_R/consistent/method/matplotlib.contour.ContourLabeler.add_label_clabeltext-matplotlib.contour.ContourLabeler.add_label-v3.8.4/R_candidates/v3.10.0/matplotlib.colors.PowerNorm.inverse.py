    def inverse(self, value):
        if not self.scaled():
            raise ValueError("Not invertible until scaled")

        result, is_scalar = self.process_value(value)

        gamma = self.gamma
        vmin, vmax = self.vmin, self.vmax

        resdat = result.data
        resdat[resdat > 0] = np.power(resdat[resdat > 0], 1 / gamma)
        resdat *= (vmax - vmin)
        resdat += vmin

        result = np.ma.array(resdat, mask=result.mask, copy=False)
        if is_scalar:
            result = result[0]
        return result
