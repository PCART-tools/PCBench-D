    def __init__(self, tarfile, file):
        """
        Create file object.

        :param tarfile: Name of TAR file.
        :param file: Name of member file.
        """
        self.fh = open(tarfile, "rb")

        while True:
            s = self.fh.read(512)
            if len(s) != 512:
                msg = "unexpected end of tar file"
                raise OSError(msg)

            name = s[:100].decode("utf-8")
            i = name.find("\0")
            if i == 0:
                msg = "cannot find subfile"
                raise OSError(msg)
            if i > 0:
                name = name[:i]

            size = int(s[124:135], 8)

            if file == name:
                break

            self.fh.seek((size + 511) & (~511), io.SEEK_CUR)

        # Open region
        super().__init__(self.fh, self.fh.tell(), size)
