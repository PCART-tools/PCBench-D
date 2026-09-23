    @property
    def resolve(self):
        """Do DNS lookup for host name?"""
        warnings.warn((".resolve property is deprecated, "
                       "use .dns_cache instead"),
                      DeprecationWarning, stacklevel=2)
        return self.use_dns_cache
