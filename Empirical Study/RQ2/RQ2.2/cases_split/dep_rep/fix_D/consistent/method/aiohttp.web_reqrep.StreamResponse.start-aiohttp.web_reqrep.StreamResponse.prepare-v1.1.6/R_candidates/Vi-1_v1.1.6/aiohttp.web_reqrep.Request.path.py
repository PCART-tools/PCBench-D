    @reify
    def path(self):
        """The URL including *PATH INFO* without the host or scheme.

        E.g., ``/app/blog``
        """
        warnings.warn("path property is deprecated, use .rel_url.path instead",
                      DeprecationWarning)
        return self.rel_url.path
