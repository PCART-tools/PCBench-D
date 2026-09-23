    def is_available(self, name):
        """
        Check if given writer is available by name.

        Parameters
        ----------
        name : str

        Returns
        -------
        available : bool
        """
        try:
            cls = self._registered[name]
        except KeyError:
            return False
        return cls.isAvailable()
