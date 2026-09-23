    def _apply_content_transfer_encoding(self, stream):
        encoding = self.headers[CONTENT_TRANSFER_ENCODING].lower()
        if encoding == 'base64':
            buffer = bytearray()
            while True:
                if buffer:
                    div, mod = divmod(len(buffer), 3)
                    chunk, buffer = buffer[:div * 3], buffer[div * 3:]
                    if chunk:
                        yield base64.b64encode(chunk)
                chunk = next(stream, None)
                if not chunk:
                    if buffer:
                        yield base64.b64encode(buffer[:])
                    return
                buffer.extend(chunk)
        elif encoding == 'quoted-printable':
            for chunk in stream:
                yield binascii.b2a_qp(chunk)
        elif encoding == 'binary':
            yield from stream
        else:
            raise RuntimeError('unknown content transfer encoding: {}'
                               ''.format(encoding))
