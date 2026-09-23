    @abc.abstractmethod  # pragma: no branch
    def url(self, **kwargs):
        """Construct url for resource with additional params.

        Deprecated, use url_for() instead.

        """
        warnings.warn(".url(...) is deprecated, use .url_for instead",
                      DeprecationWarning,
                      stacklevel=3)
