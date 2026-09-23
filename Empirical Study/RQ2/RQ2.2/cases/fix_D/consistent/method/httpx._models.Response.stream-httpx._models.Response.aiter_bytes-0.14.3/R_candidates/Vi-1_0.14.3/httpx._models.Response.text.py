    @property
    def text(self) -> str:
        if not hasattr(self, "_text"):
            content = self.content
            if not content:
                self._text = ""
            else:
                encoding = self.encoding
                self._text = content.decode(encoding, errors="replace")
        return self._text
