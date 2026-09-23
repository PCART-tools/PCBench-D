    def __init__(self, buf: IO[bytes]) -> None:
        """
        Parse image from file-like object containing ico file data
        """

        # check magic
        s = buf.read(6)
        if not _accept(s):
            msg = "not an ICO file"
            raise SyntaxError(msg)

        self.buf = buf
        self.entry = []

        # Number of items in file
        self.nb_items = i16(s, 4)

        # Get headers for each item
        for i in range(self.nb_items):
            s = buf.read(16)

            # See Wikipedia
            width = s[0] or 256
            height = s[1] or 256

            # No. of colors in image (0 if >=8bpp)
            nb_color = s[2]
            bpp = i16(s, 6)
            icon_header = IconHeader(
                width=width,
                height=height,
                nb_color=nb_color,
                reserved=s[3],
                planes=i16(s, 4),
                bpp=i16(s, 6),
                size=i32(s, 8),
                offset=i32(s, 12),
                dim=(width, height),
                square=width * height,
                # See Wikipedia notes about color depth.
                # We need this just to differ images with equal sizes
                color_depth=bpp or (nb_color != 0 and ceil(log(nb_color, 2))) or 256,
            )

            self.entry.append(icon_header)

        self.entry = sorted(self.entry, key=lambda x: x.color_depth)
        # ICO images are usually squares
        self.entry = sorted(self.entry, key=lambda x: x.square, reverse=True)
