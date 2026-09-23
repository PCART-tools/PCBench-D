    def text(self, xy: tuple[int, int], text: str) -> None:
        """
        Draws text at the given position. You must use
        :py:meth:`~PIL.PSDraw.PSDraw.setfont` before calling this method.
        """
        text_bytes = bytes(text, "UTF-8")
        text_bytes = b"\\(".join(text_bytes.split(b"("))
        text_bytes = b"\\)".join(text_bytes.split(b")"))
        self.fp.write(b"%d %d M (%s) S\n" % (xy + (text_bytes,)))
