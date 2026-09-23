    @property
    def url(self) -> typing.Optional[URL]:
        """
        Returns the URL for which the request was made.
        """
        return self.request.url
