    def url(self, *, query=None):
        return self._append_query(self._path, query)
