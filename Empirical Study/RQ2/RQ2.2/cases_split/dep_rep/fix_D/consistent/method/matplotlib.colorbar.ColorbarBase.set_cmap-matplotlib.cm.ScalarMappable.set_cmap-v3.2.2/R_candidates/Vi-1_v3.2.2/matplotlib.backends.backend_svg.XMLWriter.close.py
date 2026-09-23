    def close(self, id):
        """
        Closes open elements, up to (and including) the element identified
        by the given identifier.

        Parameters
        ----------
        id
            Element identifier, as returned by the :meth:`start` method.
        """
        while len(self.__tags) > id:
            self.end()
