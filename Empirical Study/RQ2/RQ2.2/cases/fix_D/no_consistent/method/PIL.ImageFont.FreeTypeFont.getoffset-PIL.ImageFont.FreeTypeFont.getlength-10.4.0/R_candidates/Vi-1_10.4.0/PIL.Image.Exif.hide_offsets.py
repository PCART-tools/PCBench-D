    def hide_offsets(self) -> None:
        for tag in (ExifTags.IFD.Exif, ExifTags.IFD.GPSInfo):
            if tag in self:
                self._hidden_data[tag] = self[tag]
                del self[tag]
