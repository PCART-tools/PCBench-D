    def _construct_axes_dict(self, axes=None, **kwargs):
        """Return an axes dictionary for myself."""
        d = {a: self._get_axis(a) for a in (axes or self._AXIS_ORDERS)}
        d.update(kwargs)
        return d
