    def __exit__(
        self,
        exc_type: typing.Type[BaseException] = None,
        exc_value: BaseException = None,
        traceback: TracebackType = None,
    ) -> None:
        assert isinstance(self.client, Client)
        self.response.close()
        if self.close_client:
            self.client.close()
