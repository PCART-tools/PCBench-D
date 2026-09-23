    def text(self, xy, text):
        """
        Draws text at the given position. You must use
        :py:meth:`~PIL.PSDraw.PSDraw.setfont` before calling this method.
        """
        text = bytes(text, "UTF-8")
        text = b"\\(".join(text.split(b"("))
        text = b"\\)".join(text.split(b")"))
        xy += (text,)
        self.fp.write(b"%d %d M (%s) S\n" % xy)
