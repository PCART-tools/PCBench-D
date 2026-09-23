    def set_alpha(self, alpha):
        super().set_alpha(alpha)
        _set_rgba(
            self.ctx, self._rgb, self.get_alpha(), self.get_forced_alpha())
