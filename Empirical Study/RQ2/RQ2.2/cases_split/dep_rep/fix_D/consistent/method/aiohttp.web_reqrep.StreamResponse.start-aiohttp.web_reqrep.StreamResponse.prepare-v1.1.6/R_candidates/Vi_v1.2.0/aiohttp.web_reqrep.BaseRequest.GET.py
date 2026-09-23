    @reify
    def GET(self):
        """A multidict with all the variables in the query string.

        Lazy property.
        """
        warnings.warn("GET property is deprecated, use .rel_url.query instead",
                      DeprecationWarning)
        return self.rel_url.query
