    def _get_unit(self):
        """
        Return how many days a unit of the locator is; used for
        intelligent autoscaling.
        """
        freq = self.rule._rrule._freq
        return self.get_unit_generic(freq)
