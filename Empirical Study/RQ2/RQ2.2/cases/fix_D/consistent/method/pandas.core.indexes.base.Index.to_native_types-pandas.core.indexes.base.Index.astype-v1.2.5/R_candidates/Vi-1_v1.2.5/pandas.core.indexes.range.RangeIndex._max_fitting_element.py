    def _max_fitting_element(self, upper_limit: int) -> int:
        """Returns the largest element smaller than or equal to the limit"""
        no_steps = (upper_limit - self.start) // abs(self.step)
        return self.start + abs(self.step) * no_steps
