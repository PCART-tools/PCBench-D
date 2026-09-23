    def get_child_images(self) -> list[ImageFile.ImageFile]:
        child_images = []
        exif = self.getexif()
        ifds = []
        if ExifTags.Base.SubIFDs in exif:
            subifd_offsets = exif[ExifTags.Base.SubIFDs]
            if subifd_offsets:
                if not isinstance(subifd_offsets, tuple):
                    subifd_offsets = (subifd_offsets,)
                for subifd_offset in subifd_offsets:
                    ifds.append((exif._get_ifd_dict(subifd_offset), subifd_offset))
        ifd1 = exif.get_ifd(ExifTags.IFD.IFD1)
        if ifd1 and ifd1.get(513):
            ifds.append((ifd1, exif._info.next))

        offset = None
        for ifd, ifd_offset in ifds:
            current_offset = self.fp.tell()
            if offset is None:
                offset = current_offset

            fp = self.fp
            thumbnail_offset = ifd.get(513)
            if thumbnail_offset is not None:
                thumbnail_offset += getattr(self, "_exif_offset", 0)
                self.fp.seek(thumbnail_offset)
                data = self.fp.read(ifd.get(514))
                fp = io.BytesIO(data)

            with open(fp) as im:
                from . import TiffImagePlugin

                if thumbnail_offset is None and isinstance(
                    im, TiffImagePlugin.TiffImageFile
                ):
                    im._frame_pos = [ifd_offset]
                    im._seek(0)
                im.load()
                child_images.append(im)

        if offset is not None:
            self.fp.seek(offset)
        return child_images
