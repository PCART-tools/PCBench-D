    def update_fingerprint(self, fingerprint):
        if fingerprint:
            digestlen = len(fingerprint)
            hashfunc = HASHFUNC_BY_DIGESTLEN.get(digestlen)
            if not hashfunc:
                raise ValueError('fingerprint has invalid length')
            elif hashfunc is md5 or hashfunc is sha1:
                warnings.warn('md5 and sha1 are insecure and deprecated. '
                              'Use sha256.',
                              DeprecationWarning, stacklevel=2)
                client_logger.warn('md5 and sha1 are insecure and deprecated. '
                                   'Use sha256.')
            self._hashfunc = hashfunc
        self._fingerprint = fingerprint
