    def set_alpha(self, alpha):
        # docstring inherited
        super().set_alpha(alpha)
        if self._gapcolor is not None:
            self.set_gapcolor(self._original_gapcolor)
