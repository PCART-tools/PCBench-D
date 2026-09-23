    @staticmethod
    def _extract_axes(self, data, axes, **kwargs):
        """
        Return a list of the axis indices.
        """
        return [self._extract_axis(self, data, axis=i, **kwargs)
                for i, a in enumerate(axes)]
