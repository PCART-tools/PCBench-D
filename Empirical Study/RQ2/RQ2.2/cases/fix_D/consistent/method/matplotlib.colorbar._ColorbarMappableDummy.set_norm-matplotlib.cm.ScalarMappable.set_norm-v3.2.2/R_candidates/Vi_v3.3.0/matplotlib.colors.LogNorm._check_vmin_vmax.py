    def _check_vmin_vmax(self):
        if self.vmin > self.vmax:
            raise ValueError("minvalue must be less than or equal to maxvalue")
        elif self.vmin <= 0:
            raise ValueError("minvalue must be positive")
