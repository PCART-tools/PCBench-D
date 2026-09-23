    def tobytes(self, offset: int = 8) -> bytes:
        from . import TiffImagePlugin

        head = self._get_head()
        ifd = TiffImagePlugin.ImageFileDirectory_v2(ifh=head)
        for tag, value in self.items():
            if tag in [
                ExifTags.IFD.Exif,
                ExifTags.IFD.GPSInfo,
            ] and not isinstance(value, dict):
                value = self.get_ifd(tag)
                if (
                    tag == ExifTags.IFD.Exif
                    and ExifTags.IFD.Interop in value
                    and not isinstance(value[ExifTags.IFD.Interop], dict)
                ):
                    value = value.copy()
                    value[ExifTags.IFD.Interop] = self.get_ifd(ExifTags.IFD.Interop)
            ifd[tag] = value
        return b"Exif\x00\x00" + head + ifd.tobytes(offset)
