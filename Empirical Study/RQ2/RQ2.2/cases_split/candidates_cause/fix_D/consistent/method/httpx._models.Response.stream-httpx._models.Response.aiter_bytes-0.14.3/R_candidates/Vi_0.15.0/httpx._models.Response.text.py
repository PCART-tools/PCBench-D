    @property
    def text(self) -> str:
        if not hasattr(self, "_text"):
            content = self.content
            if not content:
                self._text = ""
            else:
                decoder = TextDecoder(encoding=self.encoding)
                self._text = "".join([decoder.decode(self.content), decoder.flush()])
        return self._text
