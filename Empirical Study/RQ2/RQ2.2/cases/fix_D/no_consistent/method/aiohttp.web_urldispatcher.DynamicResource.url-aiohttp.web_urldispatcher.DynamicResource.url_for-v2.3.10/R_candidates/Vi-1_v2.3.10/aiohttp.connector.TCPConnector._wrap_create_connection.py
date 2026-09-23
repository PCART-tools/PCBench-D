    @asyncio.coroutine
    def _wrap_create_connection(self, *args,
                                req, client_error=ClientConnectorError,
                                **kwargs):
        try:
            return (yield from self._loop.create_connection(*args, **kwargs))
        except certificate_errors as exc:
            raise ClientConnectorCertificateError(
                req.connection_key, exc) from exc
        except ssl_errors as exc:
            raise ClientConnectorSSLError(req.connection_key, exc) from exc
        except OSError as exc:
            raise client_error(req.connection_key, exc) from exc
