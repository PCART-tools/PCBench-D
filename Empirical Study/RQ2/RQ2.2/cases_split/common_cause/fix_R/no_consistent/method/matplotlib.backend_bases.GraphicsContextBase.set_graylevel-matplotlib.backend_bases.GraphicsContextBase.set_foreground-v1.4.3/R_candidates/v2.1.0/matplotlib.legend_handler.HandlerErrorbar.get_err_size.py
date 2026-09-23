    def get_err_size(self, legend, xdescent, ydescent, width, height, fontsize):
        xerr_size = self._xerr_size * fontsize

        if self._yerr_size is None:
            yerr_size = xerr_size
        else:
            yerr_size = self._yerr_size * fontsize

        return xerr_size, yerr_size
