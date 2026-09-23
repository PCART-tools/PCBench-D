    def set_useMathText(self, val):
        if val is None:
            self._useMathText = rcParams['axes.formatter.use_mathtext']
        else:
            self._useMathText = val
