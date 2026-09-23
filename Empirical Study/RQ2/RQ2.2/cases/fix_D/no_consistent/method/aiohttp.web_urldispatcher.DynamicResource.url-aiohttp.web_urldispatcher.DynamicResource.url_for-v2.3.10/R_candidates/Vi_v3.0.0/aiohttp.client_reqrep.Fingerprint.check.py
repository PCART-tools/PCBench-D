    def check(self, transport):
        if not transport.get_extra_info('sslcontext'):
            return
        sslobj = transport.get_extra_info('ssl_object')
        cert = sslobj.getpeercert(binary_form=True)
        got = self._hashfunc(cert).digest()
        if got != self._fingerprint:
            host, port, *_ = transport.get_extra_info('peername')
            raise ServerFingerprintMismatch(self._fingerprint,
                                            got, host, port)
