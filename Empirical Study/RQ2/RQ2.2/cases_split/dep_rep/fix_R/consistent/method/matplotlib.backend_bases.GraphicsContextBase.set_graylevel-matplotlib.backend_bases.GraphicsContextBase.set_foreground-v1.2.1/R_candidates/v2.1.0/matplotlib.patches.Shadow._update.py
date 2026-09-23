    def _update(self):
        self.update_from(self.patch)
        if self.props is not None:
            self.update(self.props)
        else:
            r, g, b, a = colors.to_rgba(self.patch.get_facecolor())
            rho = 0.3
            r = rho * r
            g = rho * g
            b = rho * b

            self.set_facecolor((r, g, b, 0.5))
            self.set_edgecolor((r, g, b, 0.5))
            self.set_alpha(0.5)
