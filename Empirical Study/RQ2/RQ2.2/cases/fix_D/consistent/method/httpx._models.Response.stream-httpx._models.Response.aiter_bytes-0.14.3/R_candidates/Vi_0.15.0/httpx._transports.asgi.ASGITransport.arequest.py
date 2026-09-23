    async def arequest(
        self,
        method: bytes,
        url: Tuple[bytes, bytes, Optional[int], bytes],
        headers: List[Tuple[bytes, bytes]] = None,
        stream: httpcore.AsyncByteStream = None,
        ext: dict = None,
    ) -> Tuple[int, List[Tuple[bytes, bytes]], httpcore.AsyncByteStream, dict]:
        headers = [] if headers is None else headers
        stream = httpcore.PlainByteStream(content=b"") if stream is None else stream

        # ASGI scope.
        scheme, host, port, full_path = url
        path, _, query = full_path.partition(b"?")
        scope = {
            "type": "http",
            "asgi": {"version": "3.0"},
            "http_version": "1.1",
            "method": method.decode(),
            "headers": headers,
            "scheme": scheme.decode("ascii"),
            "path": path.decode("ascii"),
            "query_string": query,
            "server": (host.decode("ascii"), port),
            "client": self.client,
            "root_path": self.root_path,
        }

        # Request.
        request_body_chunks = stream.__aiter__()
        request_complete = False

        # Response.
        status_code = None
        response_headers = None
        body_parts = []
        response_started = False
        response_complete = create_event()

        # ASGI callables.

        async def receive() -> dict:
            nonlocal request_complete

            if request_complete:
                await response_complete.wait()
                return {"type": "http.disconnect"}

            try:
                body = await request_body_chunks.__anext__()
            except StopAsyncIteration:
                request_complete = True
                return {"type": "http.request", "body": b"", "more_body": False}
            return {"type": "http.request", "body": body, "more_body": True}

        async def send(message: dict) -> None:
            nonlocal status_code, response_headers, response_started

            if message["type"] == "http.response.start":
                assert not response_started

                status_code = message["status"]
                response_headers = message.get("headers", [])
                response_started = True

            elif message["type"] == "http.response.body":
                assert not response_complete.is_set()
                body = message.get("body", b"")
                more_body = message.get("more_body", False)

                if body and method != b"HEAD":
                    body_parts.append(body)

                if not more_body:
                    response_complete.set()

        try:
            await self.app(scope, receive, send)
        except Exception:
            if self.raise_app_exceptions or not response_complete.is_set():
                raise

        assert response_complete.is_set()
        assert status_code is not None
        assert response_headers is not None

        stream = httpcore.PlainByteStream(content=b"".join(body_parts))
        ext = {}

        return (status_code, response_headers, stream, ext)
