    def enable_encoding(self, encoding):
        if encoding == 'base64':
            self._encoding = encoding
            self._encoding_buffer = bytearray()
        elif encoding == 'quoted-printable':
            self._encoding = 'quoted-printable'
