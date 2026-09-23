    def _open(self):
        # Header
        s = self.fp.read(1037)

        if i16(s) not in [65534, 65535]:
            msg = "Not a valid GD 2.x .gd file"
            raise SyntaxError(msg)

        self.mode = "L"  # FIXME: "P"
        self._size = i16(s, 2), i16(s, 4)

        true_color = s[6]
        true_color_offset = 2 if true_color else 0

        # transparency index
        tindex = i32(s, 7 + true_color_offset)
        if tindex < 256:
            self.info["transparency"] = tindex

        self.palette = ImagePalette.raw(
            "XBGR", s[7 + true_color_offset + 4 : 7 + true_color_offset + 4 + 256 * 4]
        )

        self.tile = [
            (
                "raw",
                (0, 0) + self.size,
                7 + true_color_offset + 4 + 256 * 4,
                ("L", 0, 1),
            )
        ]
