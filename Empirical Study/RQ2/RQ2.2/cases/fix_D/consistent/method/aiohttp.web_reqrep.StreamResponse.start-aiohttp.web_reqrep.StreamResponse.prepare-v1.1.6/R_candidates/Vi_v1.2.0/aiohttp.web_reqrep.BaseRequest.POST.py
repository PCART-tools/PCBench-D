    @reify
    def POST(self):
        """A multidict with all the variables in the POST parameters.

        post() methods has to be called before using this attribute.
        """
        warnings.warn("POST property is deprecated, use .post() instead",
                      DeprecationWarning)
        if self._post is None:
            raise RuntimeError("POST is not available before post()")
        return self._post
