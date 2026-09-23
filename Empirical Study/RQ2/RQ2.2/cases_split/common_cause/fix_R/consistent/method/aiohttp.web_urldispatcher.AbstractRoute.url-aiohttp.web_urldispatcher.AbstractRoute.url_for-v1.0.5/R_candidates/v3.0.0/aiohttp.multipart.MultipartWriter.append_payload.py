    def append_payload(self, payload):
        """Adds a new body part to multipart writer."""
        # content-type
        if CONTENT_TYPE not in payload.headers:
            payload.headers[CONTENT_TYPE] = payload.content_type

        # compression
        encoding = payload.headers.get(CONTENT_ENCODING, '').lower()
        if encoding and encoding not in ('deflate', 'gzip', 'identity'):
            raise RuntimeError('unknown content encoding: {}'.format(encoding))
        if encoding == 'identity':
            encoding = None

        # te encoding
        te_encoding = payload.headers.get(
            CONTENT_TRANSFER_ENCODING, '').lower()
        if te_encoding not in ('', 'base64', 'quoted-printable', 'binary'):
            raise RuntimeError('unknown content transfer encoding: {}'
                               ''.format(te_encoding))
        if te_encoding == 'binary':
            te_encoding = None

        # size
        size = payload.size
        if size is not None and not (encoding or te_encoding):
            payload.headers[CONTENT_LENGTH] = str(size)

        # render headers
        headers = ''.join(
            [k + ': ' + v + '\r\n' for k, v in payload.headers.items()]
        ).encode('utf-8') + b'\r\n'

        self._parts.append((payload, headers, encoding, te_encoding))
