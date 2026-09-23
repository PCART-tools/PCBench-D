    def _dt_normalize(self):
        return type(self)(pc.floor_temporal(self._pa_array, 1, "day"))
