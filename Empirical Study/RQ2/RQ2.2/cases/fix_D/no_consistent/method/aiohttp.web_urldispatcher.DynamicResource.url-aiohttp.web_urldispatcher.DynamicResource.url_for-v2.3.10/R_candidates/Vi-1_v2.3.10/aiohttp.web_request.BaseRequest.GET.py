    @property
    def GET(self):
        """A multidict with all the variables in the query string."""
        warnings.warn("GET property is deprecated, use .query instead",
                      DeprecationWarning)
        return self._rel_url.query
