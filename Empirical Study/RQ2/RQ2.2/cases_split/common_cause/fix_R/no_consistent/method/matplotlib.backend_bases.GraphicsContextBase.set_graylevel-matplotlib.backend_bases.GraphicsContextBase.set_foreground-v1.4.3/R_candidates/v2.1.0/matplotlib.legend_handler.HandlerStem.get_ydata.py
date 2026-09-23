    def get_ydata(self, legend, xdescent, ydescent, width, height, fontsize):
        if self._yoffsets is None:
            ydata = height * (0.5 * legend._scatteryoffsets + 0.5)
        else:
            ydata = height * np.asarray(self._yoffsets)

        return ydata
