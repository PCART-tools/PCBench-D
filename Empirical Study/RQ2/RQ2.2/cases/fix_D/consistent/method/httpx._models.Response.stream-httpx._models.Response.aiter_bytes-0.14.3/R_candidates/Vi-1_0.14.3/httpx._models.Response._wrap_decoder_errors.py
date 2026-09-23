    @contextlib.contextmanager
    def _wrap_decoder_errors(self) -> typing.Iterator[None]:
        # If the response has an associated request instance, we want decoding
        # errors to be raised as proper `httpx.DecodingError` exceptions.
        try:
            yield
        except ValueError as exc:
            if self._request is None:
                raise exc
            raise DecodingError(message=str(exc), request=self.request) from exc
