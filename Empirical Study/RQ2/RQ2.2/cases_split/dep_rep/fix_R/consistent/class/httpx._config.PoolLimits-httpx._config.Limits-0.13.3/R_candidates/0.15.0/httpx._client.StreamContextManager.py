class StreamContextManager:
    def __init__(
        self,
        client: BaseClient,
        request: Request,
        *,
        auth: AuthTypes = None,
        allow_redirects: bool = True,
        timeout: typing.Union[TimeoutTypes, UnsetType] = UNSET,
        close_client: bool = False,
    ) -> None:
        self.client = client
        self.request = request
        self.auth = auth
        self.allow_redirects = allow_redirects
        self.timeout = timeout
        self.close_client = close_client

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

    async def __aenter__(self) -> "Response":
        assert isinstance(self.client, AsyncClient)
        self.response = await self.client.send(
            request=self.request,
            auth=self.auth,
            allow_redirects=self.allow_redirects,
            timeout=self.timeout,
            stream=True,
        )
        return self.response

    async def __aexit__(
        self,
        exc_type: typing.Type[BaseException] = None,
        exc_value: BaseException = None,
        traceback: TracebackType = None,
    ) -> None:
        assert isinstance(self.client, AsyncClient)
        await self.response.aclose()
