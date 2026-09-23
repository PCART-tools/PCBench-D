    def inverse(self, value):
        if not self.scaled():
            raise ValueError("Not invertible until both vmin and vmax are set")
        (vmin,), _ = self.process_value(self.vmin)
        (vmax,), _ = self.process_value(self.vmax)
        (vcenter,), _ = self.process_value(self.vcenter)
        result = np.interp(value, [0, 0.5, 1], [vmin, vcenter, vmax],
                           left=-np.inf, right=np.inf)
        return result
