    def remove(self, a):
        self.clean()

        mapping = self._mapping
        seta = mapping.pop(ref(a), None)
        if seta is not None:
            seta.remove(ref(a))
