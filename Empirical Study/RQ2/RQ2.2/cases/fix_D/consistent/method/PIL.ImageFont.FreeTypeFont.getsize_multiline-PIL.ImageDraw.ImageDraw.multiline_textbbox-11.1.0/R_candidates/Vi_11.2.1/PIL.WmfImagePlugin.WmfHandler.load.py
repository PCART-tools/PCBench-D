        def load(self, im: ImageFile.StubImageFile) -> Image.Image:
            im.fp.seek(0)  # rewind
            return Image.frombytes(
                "RGB",
                im.size,
                Image.core.drawwmf(im.fp.read(), im.size, self.bbox),
                "raw",
                "BGR",
                (im.size[0] * 3 + 3) & -4,
                -1,
            )
