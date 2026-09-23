    def joined(self, a, b):
        """
        Returns True if *a* and *b* are members of the same set.
        """
        self.clean()

        mapping = self._mapping
        try:
            return mapping[ref(a)] is mapping[ref(b)]
        except KeyError:
            return False
