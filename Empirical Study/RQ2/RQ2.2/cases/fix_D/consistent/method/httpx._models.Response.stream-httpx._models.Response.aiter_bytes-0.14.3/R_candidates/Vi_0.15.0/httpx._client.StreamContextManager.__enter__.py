    def __enter__(self) -> "Response":
        assert isinstance(self.client, Client)
        self.response = self.client.send(
            request=self.request,
            auth=self.auth,
            allow_redirects=self.allow_redirects,
            timeout=self.timeout,
            stream=True,
        )
        return self.response
