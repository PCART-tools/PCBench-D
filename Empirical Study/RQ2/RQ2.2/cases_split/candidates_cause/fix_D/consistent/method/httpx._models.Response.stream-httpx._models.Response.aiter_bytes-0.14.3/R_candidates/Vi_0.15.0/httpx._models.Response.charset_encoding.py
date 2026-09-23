    @property
    def charset_encoding(self) -> typing.Optional[str]:
        """
        Return the encoding, as specified by the Content-Type header.
        """
        content_type = self.headers.get("Content-Type")
        if content_type is None:
            return None

        _, params = cgi.parse_header(content_type)
        if "charset" not in params:
            return None

        return params["charset"].strip("'\"")
