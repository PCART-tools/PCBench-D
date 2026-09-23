    def _set_binner(self):
        """
        setup our binners
        cache these as we are an immutable object
        """

        if self.binner is None:
            self.binner, self.grouper = self._get_binner()
