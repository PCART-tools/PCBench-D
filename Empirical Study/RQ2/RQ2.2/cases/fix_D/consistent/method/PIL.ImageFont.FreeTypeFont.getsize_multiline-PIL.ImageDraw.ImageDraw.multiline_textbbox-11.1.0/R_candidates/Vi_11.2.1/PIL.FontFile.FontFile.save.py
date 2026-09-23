    def save(self, filename: str) -> None:
        """Save font"""

        self.compile()

        # font data
        if not self.bitmap:
            msg = "No bitmap created"
            raise ValueError(msg)
        self.bitmap.save(os.path.splitext(filename)[0] + ".pbm", "PNG")

        # font metrics
        with open(os.path.splitext(filename)[0] + ".pil", "wb") as fp:
            fp.write(b"PILfont\n")
            fp.write(f";;;;;;{self.ysize};\n".encode("ascii"))  # HACK!!!
            fp.write(b"DATA\n")
            for id in range(256):
                m = self.metrics[id]
                if not m:
                    puti16(fp, (0,) * 10)
                else:
                    puti16(fp, m[0] + m[1] + m[2])
