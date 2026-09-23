    @property
    def is_ssl(self) -> bool:
        message = 'URL.is_ssl() is pending deprecation. Use url.scheme == "https"'
        warnings.warn(message, DeprecationWarning)
        return self.scheme == "https"
