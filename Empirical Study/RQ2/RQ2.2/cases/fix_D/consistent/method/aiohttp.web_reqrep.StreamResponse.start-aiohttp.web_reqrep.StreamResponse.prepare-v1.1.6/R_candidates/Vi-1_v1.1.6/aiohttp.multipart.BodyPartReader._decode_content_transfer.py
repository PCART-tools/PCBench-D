    def _decode_content_transfer(self, data):
        encoding = self.headers[CONTENT_TRANSFER_ENCODING].lower()

        if encoding == 'base64':
            return base64.b64decode(data)
        elif encoding == 'quoted-printable':
            return binascii.a2b_qp(data)
        elif encoding == 'binary':
            return data
        else:
            raise RuntimeError('unknown content transfer encoding: {}'
                               ''.format(encoding))
