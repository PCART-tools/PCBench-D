    def get_matrix(self):
        if self._invalid:
            if self.mode == 'rlabel':
                angle = (
                    np.deg2rad(self.axes.get_rlabel_position()) *
                    self.axes.get_theta_direction() +
                    self.axes.get_theta_offset()
                )
            else:
                if self.mode == 'min':
                    angle = self.axes._realViewLim.xmin
                elif self.mode == 'max':
                    angle = self.axes._realViewLim.xmax

            if self.mode in ('rlabel', 'min'):
                padx = np.cos(angle - np.pi / 2)
                pady = np.sin(angle - np.pi / 2)
            else:
                padx = np.cos(angle + np.pi / 2)
                pady = np.sin(angle + np.pi / 2)

            self._t = (self.pad * padx / 72, self.pad * pady / 72)
        return mtransforms.ScaledTranslation.get_matrix(self)
