    def _load_pilfont_data(self, file: IO[bytes], image: Image.Image) -> None:
        # read PILfont header
        if file.readline() != b"PILfont\n":
            msg = "Not a PILfont file"
            raise SyntaxError(msg)
        file.readline().split(b";")
        self.info = []  # FIXME: should be a dictionary
        while True:
            s = file.readline()
            if not s or s == b"DATA\n":
                break
            self.info.append(s)

        # read PILfont metrics
        data = file.read(256 * 20)

        # check image
        if image.mode not in ("1", "L"):
            msg = "invalid font image mode"
            raise TypeError(msg)

        image.load()

        self.font = Image.core.font(image.im, data)
