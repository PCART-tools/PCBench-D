    def _getexif(self) -> dict[int, Any] | None:
        if "exif" not in self.info:
            return None
        return self.getexif()._get_merged_dict()
