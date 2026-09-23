    def _load_pilfont(self, filename: str) -> None:
        with open(filename, "rb") as fp:
            image: ImageFile.ImageFile | None = None
            root = os.path.splitext(filename)[0]

            for ext in (".png", ".gif", ".pbm"):
                if image:
                    image.close()
                try:
                    fullname = root + ext
                    image = Image.open(fullname)
                except Exception:
                    pass
                else:
                    if image and image.mode in ("1", "L"):
                        break
            else:
                if image:
                    image.close()

                msg = f"cannot find glyph data file {root}.{{gif|pbm|png}}"
                raise OSError(msg)

            self.file = fullname

            self._load_pilfont_data(fp, image)
            image.close()
