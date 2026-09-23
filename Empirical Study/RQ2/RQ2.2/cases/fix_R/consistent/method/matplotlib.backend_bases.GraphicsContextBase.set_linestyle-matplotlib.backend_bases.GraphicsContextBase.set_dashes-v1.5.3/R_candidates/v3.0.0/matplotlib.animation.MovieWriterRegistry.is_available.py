    def is_available(self, name):
        '''Check if given writer is available by name.

        Parameters
        ----------
        name : str

        Returns
        -------
        available : bool
        '''
        self.ensure_not_dirty()
        return name in self.avail
