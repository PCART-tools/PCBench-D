    @reify
    def query_string(self):
        """The query string in the URL.

        E.g., id=10
        """
        warnings.warn("query_string property is deprecated, "
                      "use .rel_url.query_string instead",
                      DeprecationWarning)
        return self.rel_url.query_string
