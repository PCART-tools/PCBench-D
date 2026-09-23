    def request(
        self,
        method: bytes,
        url: Tuple[bytes, bytes, Optional[int], bytes],
        headers: List[Tuple[bytes, bytes]] = None,
        stream: httpcore.SyncByteStream = None,
        timeout: Mapping[str, Optional[float]] = None,
    ) -> Tuple[bytes, int, bytes, List[Tuple[bytes, bytes]], httpcore.SyncByteStream]:
        headers = [] if headers is None else headers
        stream = ByteStream(b"") if stream is None else stream
        timeout = {} if timeout is None else timeout

        urllib3_timeout = urllib3.util.Timeout(
            connect=timeout.get("connect"), read=timeout.get("read")
        )

        chunked = False
        content_length = 0
        for header_key, header_value in headers:
            header_key = header_key.lower()
            if header_key == b"transfer-encoding":
                chunked = header_value == b"chunked"
            if header_key == b"content-length":
                content_length = int(header_value.decode("ascii"))
        body = stream if chunked or content_length else None

        scheme, host, port, path = url
        default_port = {b"http": 80, "https": 443}.get(scheme)
        if port is None or port == default_port:
            url_str = "%s://%s%s" % (
                scheme.decode("ascii"),
                host.decode("ascii"),
                path.decode("ascii"),
            )
        else:
            url_str = "%s://%s:%d%s" % (
                scheme.decode("ascii"),
                host.decode("ascii"),
                port,
                path.decode("ascii"),
            )

        with map_exceptions(
            {
                MaxRetryError: NetworkError,
                SSLError: NetworkError,
                socket.error: NetworkError,
            }
        ):
            conn = self.pool.urlopen(
                method=method.decode(),
                url=url_str,
                headers={
                    key.decode("ascii"): value.decode("ascii") for key, value in headers
                },
                body=body,
                redirect=False,
                assert_same_host=False,
                retries=0,
                preload_content=False,
                chunked=chunked,
                timeout=urllib3_timeout,
                pool_timeout=timeout.get("pool"),
            )

        def response_bytes() -> Iterator[bytes]:
            with map_exceptions({socket.error: NetworkError}):
                for chunk in conn.stream(4096, decode_content=False):
                    yield chunk

        status_code = conn.status
        headers = list(conn.headers.items())
        response_stream = IteratorStream(
            iterator=response_bytes(), close_func=conn.release_conn
        )
        return (b"HTTP/1.1", status_code, conn.reason, headers, response_stream)
