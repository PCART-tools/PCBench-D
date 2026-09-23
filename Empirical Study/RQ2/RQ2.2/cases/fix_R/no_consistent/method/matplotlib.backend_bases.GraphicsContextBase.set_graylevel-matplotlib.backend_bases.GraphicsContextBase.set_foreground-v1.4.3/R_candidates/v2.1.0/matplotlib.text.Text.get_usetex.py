    def get_usetex(self):
        """
        Return whether this `Text` object will render using TeX.

        If the user has not manually set this value, it will default to
        the value of `rcParams['text.usetex']`
        """
        if self._usetex is None:
            return rcParams['text.usetex']
        else:
            return self._usetex
