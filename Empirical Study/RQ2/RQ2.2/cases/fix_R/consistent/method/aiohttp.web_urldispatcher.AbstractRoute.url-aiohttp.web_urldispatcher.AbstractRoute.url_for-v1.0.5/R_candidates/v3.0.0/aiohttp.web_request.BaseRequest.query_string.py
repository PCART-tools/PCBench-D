    @property
    def query_string(self):
        """The query string in the URL.

        E.g., id=10
        """
        return self._rel_url.query_string
