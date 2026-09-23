    def list(self):
        '''Get a list of available MovieWriters.'''
        self.ensure_not_dirty()
        return list(self.avail)
