    def get_matrix(self):
        if self._invalid:
            if self.mode == 'rlabel':
                angle = (
                    np.deg2rad(self.axes.get_rlabel_position()
                               * self.axes.get_theta_direction())
                    + self.axes.get_theta_offset()
                    - np.pi / 2
                )
            elif self.mode == 'min':
                angle = self.axes._realViewLim.xmin - np.pi / 2
            elif self.mode == 'max':
                angle = self.axes._realViewLim.xmax + np.pi / 2
            self._t = (self.pad * np.cos(angle) / 72, self.pad * np.sin(angle) / 72)
        return super().get_matrix()
