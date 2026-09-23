    def copy_properties(self, other):
        """
        Copy properties of other into self.
        """
        super().copy_properties(other)
        fillcolor = getattr(other, '_fillcolor', self._fillcolor)
        effective_alphas = getattr(other, '_effective_alphas',
                                   self._effective_alphas)
        self._fillcolor = fillcolor
        self._effective_alphas = effective_alphas
