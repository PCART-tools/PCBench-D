    @reify
    def path_qs(self):
        """The URL including PATH_INFO and the query string.

        E.g, /app/blog?id=10
        """
        warnings.warn("path_qs property is deprecated, "
                      "use str(request.rel_url) instead",
                      DeprecationWarning)
        return str(self.rel_url)
