    def set_usetex(self, usetex):
        """
        Set this `Text` object to render using TeX (or not).

        If `None` is given, the option will be reset to use the value of
        `rcParams['text.usetex']`
        """
        if usetex is None:
            self._usetex = rcParams['text.usetex']
        else:
            self._usetex = bool(usetex)
        self.stale = True
