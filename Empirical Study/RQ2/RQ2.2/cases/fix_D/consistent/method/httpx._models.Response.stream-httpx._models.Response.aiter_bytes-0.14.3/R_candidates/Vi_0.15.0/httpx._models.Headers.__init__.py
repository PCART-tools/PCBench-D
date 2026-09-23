    def __init__(self, headers: HeaderTypes = None, encoding: str = None) -> None:
        if headers is None:
            self._list = []  # type: typing.List[typing.Tuple[bytes, bytes]]
        elif isinstance(headers, Headers):
            self._list = list(headers.raw)
        elif isinstance(headers, dict):
            self._list = [
                (normalize_header_key(k, encoding), normalize_header_value(v, encoding))
                for k, v in headers.items()
            ]
        else:
            self._list = [
                (normalize_header_key(k, encoding), normalize_header_value(v, encoding))
                for k, v in headers
            ]

        self._dict = {}  # type: typing.Dict[bytes, bytes]
        for key, value in self._list:
            if key in self._dict:
                self._dict[key] = self._dict[key] + b", " + value
            else:
                self._dict[key] = value

        self._encoding = encoding
