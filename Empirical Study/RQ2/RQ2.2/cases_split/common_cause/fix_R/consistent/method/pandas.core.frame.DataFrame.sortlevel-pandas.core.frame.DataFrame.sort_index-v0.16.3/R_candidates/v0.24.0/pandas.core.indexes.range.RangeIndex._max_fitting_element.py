    def _max_fitting_element(self, upper_limit):
        """Returns the largest element smaller than or equal to the limit"""
        no_steps = (upper_limit - self._start) // abs(self._step)
        return self._start + abs(self._step) * no_steps
