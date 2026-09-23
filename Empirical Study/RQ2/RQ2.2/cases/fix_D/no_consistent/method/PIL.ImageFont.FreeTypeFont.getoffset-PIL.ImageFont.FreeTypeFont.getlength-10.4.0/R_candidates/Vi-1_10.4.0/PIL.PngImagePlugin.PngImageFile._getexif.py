    def _getexif(self) -> dict[str, Any] | None:
        if "exif" not in self.info:
            self.load()
        if "exif" not in self.info and "Raw profile type exif" not in self.info:
            return None
        return self.getexif()._get_merged_dict()
