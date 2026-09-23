    def getexif(self):
        if "exif" not in self.info:
            self.load()

        return super().getexif()
