    @property
    def query(self):
        """A multidict with all the variables in the query string."""
        return self._rel_url.query
