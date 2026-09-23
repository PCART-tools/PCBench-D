    def get_siblings(self, a):
        """
        Returns all of the items joined with *a*, including itself.
        """
        self.clean()

        siblings = self._mapping.get(ref(a), [ref(a)])
        return [x() for x in siblings]
