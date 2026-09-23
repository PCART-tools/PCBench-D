    def set_usetex(self, val):
        if val is None:
            self._usetex = rcParams['text.usetex']
        else:
            self._usetex = val
