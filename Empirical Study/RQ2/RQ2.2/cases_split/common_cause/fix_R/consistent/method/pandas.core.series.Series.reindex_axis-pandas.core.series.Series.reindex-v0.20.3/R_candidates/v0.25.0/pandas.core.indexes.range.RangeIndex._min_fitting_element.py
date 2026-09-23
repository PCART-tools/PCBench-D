    def _min_fitting_element(self, lower_limit):
        """Returns the smallest element greater than or equal to the limit"""
        no_steps = -(-(lower_limit - self.start) // abs(self.step))
        return self.start + abs(self.step) * no_steps
