    def getcolor(
        self,
        color: tuple[int, ...],
        image: Image.Image | None = None,
    ) -> int:
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
                index = self._new_color_index(image, e)
                assert isinstance(self._palette, bytearray)
                self.colors[color] = index
                if index * 3 < len(self.palette):
                    self._palette = (
                        self._palette[: index * 3]
                        + bytes(color)
                        + self._palette[index * 3 + 3 :]
                    )
                else:
                    self._palette += bytes(color)
                self.dirty = 1
                return index
        else:
            msg = f"unknown color specifier: {repr(color)}"  # type: ignore[unreachable]
            raise ValueError(msg)
