    def getcolor(self, color, image=None):
        """Given an rgb tuple, allocate palette entry.

        .. warning:: This method is experimental.
        """
        if self.rawmode:
            msg = "palette contains raw palette data"
            raise ValueError(msg)
        if isinstance(color, tuple):
            if self.mode == "RGB":
                if len(color) == 4:
                    if color[3] != 255:
                        msg = "cannot add non-opaque RGBA color to RGB palette"
                        raise ValueError(msg)
                    color = color[:3]
            elif self.mode == "RGBA":
                if len(color) == 3:
                    color += (255,)
            try:
                return self.colors[color]
            except KeyError as e:
                # allocate new color slot
                if not isinstance(self.palette, bytearray):
                    self._palette = bytearray(self.palette)
                index = len(self.palette) // 3
                special_colors = ()
                if image:
                    special_colors = (
                        image.info.get("background"),
                        image.info.get("transparency"),
                    )
                while index in special_colors:
                    index += 1
                if index >= 256:
                    if image:
                        # Search for an unused index
                        for i, count in reversed(list(enumerate(image.histogram()))):
                            if count == 0 and i not in special_colors:
                                index = i
                                break
                    if index >= 256:
                        msg = "cannot allocate more than 256 colors"
                        raise ValueError(msg) from e
                self.colors[color] = index
                if index * 3 < len(self.palette):
                    self._palette = (
                        self.palette[: index * 3]
                        + bytes(color)
                        + self.palette[index * 3 + 3 :]
                    )
                else:
                    self._palette += bytes(color)
                self.dirty = 1
                return index
        else:
            msg = f"unknown color specifier: {repr(color)}"
            raise ValueError(msg)
