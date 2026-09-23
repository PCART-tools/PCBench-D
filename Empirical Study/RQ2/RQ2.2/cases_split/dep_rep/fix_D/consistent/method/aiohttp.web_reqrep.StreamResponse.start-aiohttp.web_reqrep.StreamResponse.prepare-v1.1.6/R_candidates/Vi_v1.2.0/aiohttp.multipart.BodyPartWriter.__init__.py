    def __init__(self, obj, headers=None, *, chunk_size=8192):
        if headers is None:
            headers = CIMultiDict()
        elif not isinstance(headers, CIMultiDict):
            headers = CIMultiDict(headers)

        self.obj = obj
        self.headers = headers
        self._chunk_size = chunk_size
        self._fill_headers_with_defaults()

        self._serialize_map = {
            bytes: self._serialize_bytes,
            str: self._serialize_str,
            io.IOBase: self._serialize_io,
            MultipartWriter: self._serialize_multipart,
            ('application', 'json'): self._serialize_json,
            ('application', 'x-www-form-urlencoded'): self._serialize_form
        }
