    @staticmethod
    def _construct_axes_dict_from(self, axes, **kwargs):
        """ return an axes dictionary for the passed axes """
        d = dict([(a, ax) for a, ax in zip(self._AXIS_ORDERS, axes)])
        d.update(kwargs)
        return d
