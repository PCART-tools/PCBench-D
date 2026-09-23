    @reify
    def scheme(self):
        """A string representing the scheme of the request.

        'http' or 'https'.
        """
        warnings.warn("path_qs property is deprecated, "
                      "use .url.scheme instead",
                      DeprecationWarning)
        return self.url.scheme
