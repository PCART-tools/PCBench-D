    def _gen_axes_spines(self):
        spines = {
            'polar': Spine.arc_spine(self, 'top', (0.5, 0.5), 0.5, 0, 360),
            'start': Spine.linear_spine(self, 'left'),
            'end': Spine.linear_spine(self, 'right'),
            'inner': Spine.arc_spine(self, 'bottom', (0.5, 0.5), 0.0, 0, 360),
        }
        spines['polar'].set_transform(self.transWedge + self.transAxes)
        spines['inner'].set_transform(self.transWedge + self.transAxes)
        spines['start'].set_transform(self._yaxis_transform)
        spines['end'].set_transform(self._yaxis_transform)
        return spines
