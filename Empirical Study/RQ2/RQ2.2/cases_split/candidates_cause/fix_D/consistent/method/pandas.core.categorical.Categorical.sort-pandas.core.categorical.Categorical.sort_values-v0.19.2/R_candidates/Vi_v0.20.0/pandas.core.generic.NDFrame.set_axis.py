    def set_axis(self, axis, labels):
        """ public verson of axis assignment """
        setattr(self, self._get_axis_name(axis), labels)
