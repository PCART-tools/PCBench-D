    def get_usetex(self):
        """
        Return whether this `Text` object uses TeX for rendering.

        If the user has not manually set this value, it defaults to
        :rc:`text.usetex`.
        """
        if self._usetex is None:
            return rcParams['text.usetex']
        else:
            return self._usetex
