    def _do_start_compression(self, coding):
        if self._body_payload or self._chunked:
            return super()._do_start_compression(coding)
        if coding != ContentCoding.identity:
            # Instead of using _payload_writer.enable_compression,
            # compress the whole body
            zlib_mode = (16 + zlib.MAX_WBITS
                         if coding.value == 'gzip' else -zlib.MAX_WBITS)
            compressobj = zlib.compressobj(wbits=zlib_mode)
            self._compressed_body = compressobj.compress(self._body) +\
                compressobj.flush()
            self._headers[hdrs.CONTENT_ENCODING] = coding.value
            self._headers[hdrs.CONTENT_LENGTH] = \
                str(len(self._compressed_body))
