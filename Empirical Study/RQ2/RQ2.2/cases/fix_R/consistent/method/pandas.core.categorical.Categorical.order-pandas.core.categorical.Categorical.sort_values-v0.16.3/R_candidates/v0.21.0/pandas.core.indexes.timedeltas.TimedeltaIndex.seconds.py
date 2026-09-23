    @property
    def seconds(self):
        """ Number of seconds (>= 0 and less than 1 day) for each element. """
        return self._get_field('seconds')
