    def _reload_exif(self):
        if self._exif is None or not self._exif._loaded:
            return
        self._exif._loaded = False
        self.getexif()
