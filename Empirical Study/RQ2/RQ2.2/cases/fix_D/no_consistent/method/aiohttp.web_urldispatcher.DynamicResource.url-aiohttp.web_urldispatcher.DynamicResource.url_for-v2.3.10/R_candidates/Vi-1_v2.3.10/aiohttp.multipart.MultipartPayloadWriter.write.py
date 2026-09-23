    @asyncio.coroutine
    def write(self, chunk):
        if self._compress is not None:
            if chunk:
                chunk = self._compress.compress(chunk)
                if not chunk:
                    return

        if self._encoding == 'base64':
            self._encoding_buffer.extend(chunk)

            if self._encoding_buffer:
                buffer = self._encoding_buffer
                div, mod = divmod(len(buffer), 3)
                enc_chunk, self._encoding_buffer = (
                    buffer[:div * 3], buffer[div * 3:])
                if enc_chunk:
                    enc_chunk = base64.b64encode(enc_chunk)
                    yield from self._writer.write(enc_chunk)
        elif self._encoding == 'quoted-printable':
            yield from self._writer.write(binascii.b2a_qp(chunk))
        else:
            yield from self._writer.write(chunk)
