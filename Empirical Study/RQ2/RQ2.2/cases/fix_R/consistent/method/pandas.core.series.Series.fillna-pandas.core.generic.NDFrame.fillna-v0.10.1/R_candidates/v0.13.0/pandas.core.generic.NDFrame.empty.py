    @property
    def empty(self):
        "True if NDFrame is entirely empty [no items]"
        return not all(len(self._get_axis(a)) > 0 for a in self._AXIS_ORDERS)
