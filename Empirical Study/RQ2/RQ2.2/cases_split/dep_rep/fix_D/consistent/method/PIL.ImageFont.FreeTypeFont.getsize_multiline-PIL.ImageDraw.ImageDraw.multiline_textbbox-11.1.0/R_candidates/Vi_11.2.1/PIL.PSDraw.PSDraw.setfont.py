    def setfont(self, font: str, size: int) -> None:
        """
        Selects which font to use.

        :param font: A PostScript font name
        :param size: Size in points.
        """
        font_bytes = bytes(font, "UTF-8")
        if font_bytes not in self.isofont:
            # reencode font
            self.fp.write(
                b"/PSDraw-%s ISOLatin1Encoding /%s E\n" % (font_bytes, font_bytes)
            )
            self.isofont[font_bytes] = 1
        # rough
        self.fp.write(b"/F0 %d /PSDraw-%s F\n" % (size, font_bytes))
