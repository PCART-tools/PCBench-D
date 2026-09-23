    def _apply_content_encoding(self, stream):
        encoding = self.headers[CONTENT_ENCODING].lower()
        if encoding == 'identity':
            yield from stream
        elif encoding in ('deflate', 'gzip'):
            if encoding == 'gzip':
                zlib_mode = 16 + zlib.MAX_WBITS
            else:
                zlib_mode = -zlib.MAX_WBITS
            zcomp = zlib.compressobj(wbits=zlib_mode)
            for chunk in stream:
                yield zcomp.compress(chunk)
            else:
                yield zcomp.flush()
        else:
            raise RuntimeError('unknown content encoding: {}'
                               ''.format(encoding))
