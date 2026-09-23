    @property
    def nanoseconds(self):
        """
        Number of nanoseconds (>= 0 and less than 1 microsecond) for each
        element.
        """
        return self._get_field('nanoseconds')
