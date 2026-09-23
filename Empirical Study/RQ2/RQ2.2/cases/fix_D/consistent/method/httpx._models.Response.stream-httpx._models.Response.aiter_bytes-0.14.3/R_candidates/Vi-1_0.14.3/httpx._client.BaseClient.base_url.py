    @base_url.setter
    def base_url(self, url: URLTypes) -> None:
        self._base_url = self._enforce_trailing_slash(URL(url))
