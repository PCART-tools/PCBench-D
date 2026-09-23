class FileField:
    """
    A single file field item, within a multipart form field.
    """

    def __init__(self, name: str, value: FileTypes) -> None:
        self.name = name

        fileobj: FileContent

        if isinstance(value, tuple):
            try:
                filename, fileobj, content_type = value  # type: ignore
            except ValueError:
                filename, fileobj = value  # type: ignore
                content_type = guess_content_type(filename)
        else:
            filename = Path(str(getattr(value, "name", "upload"))).name
            fileobj = value
            content_type = guess_content_type(filename)

        self.filename = filename
        self.file = fileobj
        self.content_type = content_type
        self._consumed = False

    def get_length(self) -> int:
        headers = self.render_headers()

        if isinstance(self.file, (str, bytes)):
            return len(headers) + len(self.file)

        # Let's do our best not to read `file` into memory.
        try:
            file_length = peek_filelike_length(self.file)
        except OSError:
            # As a last resort, read file and cache contents for later.
            assert not hasattr(self, "_data")
            self._data = to_bytes(self.file.read())
            file_length = len(self._data)

        return len(headers) + file_length

    def render_headers(self) -> bytes:
        if not hasattr(self, "_headers"):
            parts = [
                b"Content-Disposition: form-data; ",
                format_form_param("name", self.name),
            ]
            if self.filename:
                filename = format_form_param("filename", self.filename)
                parts.extend([b"; ", filename])
            if self.content_type is not None:
                content_type = self.content_type.encode()
                parts.extend([b"\r\nContent-Type: ", content_type])
            parts.append(b"\r\n\r\n")
            self._headers = b"".join(parts)

        return self._headers

    def render_data(self) -> typing.Iterator[bytes]:
        if isinstance(self.file, (str, bytes)):
            yield to_bytes(self.file)
            return

        if hasattr(self, "_data"):
            # Already rendered.
            yield self._data
            return

        if self._consumed:  # pragma: nocover
            self.file.seek(0)
        self._consumed = True

        for chunk in self.file:
            yield to_bytes(chunk)

    def render(self) -> typing.Iterator[bytes]:
        yield self.render_headers()
        yield from self.render_data()
