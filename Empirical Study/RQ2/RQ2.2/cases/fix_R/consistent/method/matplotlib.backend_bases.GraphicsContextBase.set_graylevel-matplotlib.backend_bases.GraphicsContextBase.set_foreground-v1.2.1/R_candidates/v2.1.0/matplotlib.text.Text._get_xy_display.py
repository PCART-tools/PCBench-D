    def _get_xy_display(self):
        'get the (possibly unit converted) transformed x, y in display coords'
        x, y = self.get_unitless_position()
        return self.get_transform().transform_point((x, y))
