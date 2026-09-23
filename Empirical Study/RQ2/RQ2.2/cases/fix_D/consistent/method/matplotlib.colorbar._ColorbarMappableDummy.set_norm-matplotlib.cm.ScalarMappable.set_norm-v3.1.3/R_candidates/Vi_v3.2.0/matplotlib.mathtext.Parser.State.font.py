        @font.setter
        def font(self, name):
            if name == "circled":
                cbook.warn_deprecated(
                    "3.1", name="\\mathcircled", obj_type="mathtext command",
                    alternative="unicode characters (e.g. '\\N{CIRCLED LATIN "
                    "CAPITAL LETTER A}' or '\\u24b6')")
            if name in ('rm', 'it', 'bf'):
                self.font_class = name
            self._font = name
