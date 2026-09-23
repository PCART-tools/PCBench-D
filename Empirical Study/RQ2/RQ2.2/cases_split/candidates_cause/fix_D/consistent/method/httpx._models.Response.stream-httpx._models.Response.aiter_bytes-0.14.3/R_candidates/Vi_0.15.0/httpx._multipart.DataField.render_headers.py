    def render_headers(self) -> bytes:
        if not hasattr(self, "_headers"):
            name = format_form_param("name", self.name)
            self._headers = b"".join(
                [b"Content-Disposition: form-data; ", name, b"\r\n\r\n"]
            )

        return self._headers
