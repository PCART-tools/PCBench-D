    def getexif(self) -> Image.Exif:
        if "exif" not in self.info:
            self.load()

        return super().getexif()
