    def _get_merged_dict(self) -> dict[int, Any]:
        merged_dict = dict(self)

        # get EXIF extension
        if ExifTags.IFD.Exif in self:
            ifd = self._get_ifd_dict(self[ExifTags.IFD.Exif], ExifTags.IFD.Exif)
            if ifd:
                merged_dict.update(ifd)

        # GPS
        if ExifTags.IFD.GPSInfo in self:
            merged_dict[ExifTags.IFD.GPSInfo] = self._get_ifd_dict(
                self[ExifTags.IFD.GPSInfo], ExifTags.IFD.GPSInfo
            )

        return merged_dict
