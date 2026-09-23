    def view(self, cls=None):
        """ this is defined as a copy with the same identity """
        result = self.copy()
        result._id = self._id
        return result
