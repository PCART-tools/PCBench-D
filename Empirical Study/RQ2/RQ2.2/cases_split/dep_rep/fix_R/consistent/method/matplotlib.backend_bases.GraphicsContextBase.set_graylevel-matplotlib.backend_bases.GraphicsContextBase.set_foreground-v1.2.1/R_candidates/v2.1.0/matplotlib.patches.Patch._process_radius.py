    def _process_radius(self, radius):
        if radius is not None:
            return radius
        if cbook.is_numlike(self._picker):
            _radius = self._picker
        else:
            if self.get_edgecolor()[3] == 0:
                _radius = 0
            else:
                _radius = self.get_linewidth()
        return _radius
