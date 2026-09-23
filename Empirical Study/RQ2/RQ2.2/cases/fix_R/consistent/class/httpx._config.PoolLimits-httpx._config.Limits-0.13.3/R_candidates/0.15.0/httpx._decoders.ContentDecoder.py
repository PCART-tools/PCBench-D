class ContentDecoder:
    def decode(self, data: bytes) -> bytes:
        raise NotImplementedError()  # pragma: nocover

    def flush(self) -> bytes:
        raise NotImplementedError()  # pragma: nocover
