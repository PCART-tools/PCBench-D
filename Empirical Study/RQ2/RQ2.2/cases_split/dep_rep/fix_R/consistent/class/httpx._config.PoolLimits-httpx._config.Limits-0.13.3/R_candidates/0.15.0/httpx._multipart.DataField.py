class DataField:
    """
    A single form field item, within a multipart form field.
    """

    def __init__(self, name: str, value: typing.Union[str, bytes]) -> None:
        if not isinstance(name, str):
            raise TypeError("Invalid type for name. Expected str.")
        if not isinstance(value, (str, bytes)):
            raise TypeError("Invalid type for value. Expected str or bytes.")
        self.name = name
        self.value = value

    def render_headers(self) -> bytes:
        if not hasattr(self, "_headers"):
            name = format_form_param("name", self.name)
            self._headers = b"".join(
                [b"Content-Disposition: form-data; ", name, b"\r\n\r\n"]
            )

        return self._headers

    def render_data(self) -> bytes:
        if not hasattr(self, "_data"):
            self._data = (
                self.value
                if isinstance(self.value, bytes)
                else self.value.encode("utf-8")
            )

        return self._data

    def get_length(self) -> int:
        headers = self.render_headers()
        data = self.render_data()
        return len(headers) + len(data)

    def render(self) -> typing.Iterator[bytes]:
        yield self.render_headers()
        yield self.render_data()
