    def save(self, fp: str | IO[str]) -> None:
        """Save palette to text file.

        .. warning:: This method is experimental.
        """
        if self.rawmode:
            msg = "palette contains raw palette data"
            raise ValueError(msg)
        if isinstance(fp, str):
            fp = open(fp, "w")
        fp.write("# Palette\n")
        fp.write(f"# Mode: {self.mode}\n")
        for i in range(256):
            fp.write(f"{i}")
            for j in range(i * len(self.mode), (i + 1) * len(self.mode)):
                try:
                    fp.write(f" {self.palette[j]}")
                except IndexError:
                    fp.write(" 0")
            fp.write("\n")
        fp.close()
