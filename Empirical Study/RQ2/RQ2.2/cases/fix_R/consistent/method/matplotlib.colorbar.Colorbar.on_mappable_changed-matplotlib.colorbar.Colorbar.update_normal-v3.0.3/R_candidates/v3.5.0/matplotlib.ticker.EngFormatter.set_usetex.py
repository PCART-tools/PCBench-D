    def set_usetex(self, val):
        if val is None:
            self._usetex = mpl.rcParams['text.usetex']
        else:
            self._usetex = val
