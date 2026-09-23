    @property
    def microseconds(self):
        """
        Number of microseconds (>= 0 and less than 1 second) for each
        element. """
        return self._get_field('microseconds')
