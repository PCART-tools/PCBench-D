    def __init__(self, fingerprint):
        digestlen = len(fingerprint)
        hashfunc = self.HASHFUNC_BY_DIGESTLEN.get(digestlen)
        if not hashfunc:
            raise ValueError('fingerprint has invalid length')
        elif hashfunc is md5 or hashfunc is sha1:
            raise ValueError('md5 and sha1 are insecure and '
                             'not supported. Use sha256.')
        self._hashfunc = hashfunc
        self._fingerprint = fingerprint
