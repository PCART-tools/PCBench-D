    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        url_str = str(self)
        if self._uri_reference.userinfo:
            url_str = (
                rfc3986.urlparse(url_str)
                .copy_with(userinfo=f"{self.username}:[secure]")
                .unsplit()
            )
        return f"{class_name}({url_str!r})"
