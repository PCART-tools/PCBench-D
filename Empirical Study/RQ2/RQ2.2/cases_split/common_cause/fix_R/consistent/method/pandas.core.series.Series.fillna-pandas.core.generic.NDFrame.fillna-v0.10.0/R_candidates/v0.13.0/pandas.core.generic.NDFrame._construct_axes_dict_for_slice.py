    def _construct_axes_dict_for_slice(self, axes=None, **kwargs):
        """ return an axes dictionary for myself """
        d = dict([(self._AXIS_SLICEMAP[a], self._get_axis(a))
                 for a in (axes or self._AXIS_ORDERS)])
        d.update(kwargs)
        return d
