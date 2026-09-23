    def get_ifd(self, tag: int) -> dict[int, Any]:
        if tag not in self._ifds:
            if tag == ExifTags.IFD.IFD1:
                if self._info is not None and self._info.next != 0:
                    ifd = self._get_ifd_dict(self._info.next)
                    if ifd is not None:
                        self._ifds[tag] = ifd
            elif tag in [ExifTags.IFD.Exif, ExifTags.IFD.GPSInfo]:
                offset = self._hidden_data.get(tag, self.get(tag))
                if offset is not None:
                    ifd = self._get_ifd_dict(offset, tag)
                    if ifd is not None:
                        self._ifds[tag] = ifd
            elif tag in [ExifTags.IFD.Interop, ExifTags.IFD.MakerNote]:
                if ExifTags.IFD.Exif not in self._ifds:
                    self.get_ifd(ExifTags.IFD.Exif)
                tag_data = self._ifds[ExifTags.IFD.Exif][tag]
                if tag == ExifTags.IFD.MakerNote:
                    from .TiffImagePlugin import ImageFileDirectory_v2

                    if tag_data.startswith(b"FUJIFILM"):
                        ifd_offset = i32le(tag_data, 8)
                        ifd_data = tag_data[ifd_offset:]

                        makernote = {}
                        for i in range(struct.unpack("<H", ifd_data[:2])[0]):
                            ifd_tag, typ, count, data = struct.unpack(
                                "<HHL4s", ifd_data[i * 12 + 2 : (i + 1) * 12 + 2]
                            )
                            try:
                                (
                                    unit_size,
                                    handler,
                                ) = ImageFileDirectory_v2._load_dispatch[typ]
                            except KeyError:
                                continue
                            size = count * unit_size
                            if size > 4:
                                (offset,) = struct.unpack("<L", data)
                                data = ifd_data[offset - 12 : offset + size - 12]
                            else:
                                data = data[:size]

                            if len(data) != size:
                                warnings.warn(
                                    "Possibly corrupt EXIF MakerNote data.  "
                                    f"Expecting to read {size} bytes but only got "
                                    f"{len(data)}. Skipping tag {ifd_tag}"
                                )
                                continue

                            if not data:
                                continue

                            makernote[ifd_tag] = handler(
                                ImageFileDirectory_v2(), data, False
                            )
                        self._ifds[tag] = dict(self._fixup_dict(makernote))
                    elif self.get(0x010F) == "Nintendo":
                        makernote = {}
                        for i in range(struct.unpack(">H", tag_data[:2])[0]):
                            ifd_tag, typ, count, data = struct.unpack(
                                ">HHL4s", tag_data[i * 12 + 2 : (i + 1) * 12 + 2]
                            )
                            if ifd_tag == 0x1101:
                                # CameraInfo
                                (offset,) = struct.unpack(">L", data)
                                self.fp.seek(offset)

                                camerainfo: dict[str, int | bytes] = {
                                    "ModelID": self.fp.read(4)
                                }

                                self.fp.read(4)
                                # Seconds since 2000
                                camerainfo["TimeStamp"] = i32le(self.fp.read(12))

                                self.fp.read(4)
                                camerainfo["InternalSerialNumber"] = self.fp.read(4)

                                self.fp.read(12)
                                parallax = self.fp.read(4)
                                handler = ImageFileDirectory_v2._load_dispatch[
                                    TiffTags.FLOAT
                                ][1]
                                camerainfo["Parallax"] = handler(
                                    ImageFileDirectory_v2(), parallax, False
                                )[0]

                                self.fp.read(4)
                                camerainfo["Category"] = self.fp.read(2)

                                makernote = {0x1101: camerainfo}
                        self._ifds[tag] = makernote
                else:
                    # Interop
                    ifd = self._get_ifd_dict(tag_data, tag)
                    if ifd is not None:
                        self._ifds[tag] = ifd
        ifd = self._ifds.setdefault(tag, {})
        if tag == ExifTags.IFD.Exif and self._hidden_data:
            ifd = {
                k: v
                for (k, v) in ifd.items()
                if k not in (ExifTags.IFD.Interop, ExifTags.IFD.MakerNote)
            }
        return ifd
