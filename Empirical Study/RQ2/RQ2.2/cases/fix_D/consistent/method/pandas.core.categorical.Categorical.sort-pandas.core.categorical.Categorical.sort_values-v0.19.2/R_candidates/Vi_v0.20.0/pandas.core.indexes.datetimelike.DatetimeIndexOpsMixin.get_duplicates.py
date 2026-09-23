    def get_duplicates(self):
        values = Index.get_duplicates(self)
        return self._simple_new(values)
