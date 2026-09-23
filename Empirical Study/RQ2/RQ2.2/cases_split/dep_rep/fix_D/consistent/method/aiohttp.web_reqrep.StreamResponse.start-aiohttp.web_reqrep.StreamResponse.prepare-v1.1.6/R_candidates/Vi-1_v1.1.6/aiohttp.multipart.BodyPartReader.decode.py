    def decode(self, data):
        """Decodes data according the specified `Content-Encoding`
        or `Content-Transfer-Encoding` headers value.

        Supports ``gzip``, ``deflate`` and ``identity`` encodings for
        `Content-Encoding` header.

        Supports ``base64``, ``quoted-printable``, ``binary`` encodings for
        `Content-Transfer-Encoding` header.

        :param bytearray data: Data to decode.

        :raises: :exc:`RuntimeError` - if encoding is unknown.

        :rtype: bytes
        """
        if CONTENT_TRANSFER_ENCODING in self.headers:
            data = self._decode_content_transfer(data)
        if CONTENT_ENCODING in self.headers:
            return self._decode_content(data)
        return data
