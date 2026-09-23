    def get_format_mimetype(self) -> str | None:
        if self.custom_mimetype:
            return self.custom_mimetype
        if self.format is not None:
            return Image.MIME.get(self.format.upper())
        return None
