    def __init__(self, base, linthresh, linscale):
        Transform.__init__(self)
        self.base = base
        self.linthresh = linthresh
        self.linscale = linscale
        self._linscale_adj = (linscale / (1.0 - self.base ** -1))
        self._log_base = np.log(base)
