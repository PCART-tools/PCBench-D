    @reify
    def raw_path(self):
        """ The URL including raw *PATH INFO* without the host or scheme.
        Warning, the path is unquoted and may contains non valid URL characters

        E.g., ``/my%2Fpath%7Cwith%21some%25strange%24characters``
        """
        warnings.warn("raw_path property is deprecated, "
                      "use .rel_url.raw_path instead",
                      DeprecationWarning)
        return self.rel_url.raw_path
