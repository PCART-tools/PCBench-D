    @staticmethod
    def _extract_axes(self, data, axes, **kwargs):
        """ return a list of the axis indicies """
        return [self._extract_axis(self, data, axis=i, **kwargs) for i, a
                in enumerate(axes)]
