    def _min_fitting_element(self, lower_limit):
        """Returns the smallest element greater than or equal to the limit"""
        no_steps = -(-(lower_limit - self._start) // abs(self._step))
        return self._start + abs(self._step) * no_steps
