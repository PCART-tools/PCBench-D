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
