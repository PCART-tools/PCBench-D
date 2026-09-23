    def _open(self):
        (length, offset) = self._find_offset(self.fp)

        # go to offset - start of "%!PS"
        self.fp.seek(offset)

        self._mode = "RGB"
        self._size = None

        byte_arr = bytearray(255)
        bytes_mv = memoryview(byte_arr)
        bytes_read = 0
        reading_header_comments = True
        reading_trailer_comments = False
        trailer_reached = False

        def check_required_header_comments():
            if "PS-Adobe" not in self.info:
                msg = 'EPS header missing "%!PS-Adobe" comment'
                raise SyntaxError(msg)
            if "BoundingBox" not in self.info:
                msg = 'EPS header missing "%%BoundingBox" comment'
                raise SyntaxError(msg)

        def _read_comment(s):
            nonlocal reading_trailer_comments
            try:
                m = split.match(s)
            except re.error as e:
                msg = "not an EPS file"
                raise SyntaxError(msg) from e

            if m:
                k, v = m.group(1, 2)
                self.info[k] = v
                if k == "BoundingBox":
                    if v == "(atend)":
                        reading_trailer_comments = True
                    elif not self._size or (
                        trailer_reached and reading_trailer_comments
                    ):
                        try:
                            # Note: The DSC spec says that BoundingBox
                            # fields should be integers, but some drivers
                            # put floating point values there anyway.
                            box = [int(float(i)) for i in v.split()]
                            self._size = box[2] - box[0], box[3] - box[1]
                            self.tile = [
                                ("eps", (0, 0) + self.size, offset, (length, box))
                            ]
                        except Exception:
                            pass
                return True

        while True:
            byte = self.fp.read(1)
            if byte == b"":
                # if we didn't read a byte we must be at the end of the file
                if bytes_read == 0:
                    break
            elif byte in b"\r\n":
                # if we read a line ending character, ignore it and parse what
                # we have already read. if we haven't read any other characters,
                # continue reading
                if bytes_read == 0:
                    continue
            else:
                # ASCII/hexadecimal lines in an EPS file must not exceed
                # 255 characters, not including line ending characters
                if bytes_read >= 255:
                    # only enforce this for lines starting with a "%",
                    # otherwise assume it's binary data
                    if byte_arr[0] == ord("%"):
                        msg = "not an EPS file"
                        raise SyntaxError(msg)
                    else:
                        if reading_header_comments:
                            check_required_header_comments()
                            reading_header_comments = False
                        # reset bytes_read so we can keep reading
                        # data until the end of the line
                        bytes_read = 0
                byte_arr[bytes_read] = byte[0]
                bytes_read += 1
                continue

            if reading_header_comments:
                # Load EPS header

                # if this line doesn't start with a "%",
                # or does start with "%%EndComments",
                # then we've reached the end of the header/comments
                if byte_arr[0] != ord("%") or bytes_mv[:13] == b"%%EndComments":
                    check_required_header_comments()
                    reading_header_comments = False
                    continue

                s = str(bytes_mv[:bytes_read], "latin-1")
                if not _read_comment(s):
                    m = field.match(s)
                    if m:
                        k = m.group(1)
                        if k[:8] == "PS-Adobe":
                            self.info["PS-Adobe"] = k[9:]
                        else:
                            self.info[k] = ""
                    elif s[0] == "%":
                        # handle non-DSC PostScript comments that some
                        # tools mistakenly put in the Comments section
                        pass
                    else:
                        msg = "bad EPS header"
                        raise OSError(msg)
            elif bytes_mv[:11] == b"%ImageData:":
                # Check for an "ImageData" descriptor
                # https://www.adobe.com/devnet-apps/photoshop/fileformatashtml/#50577413_pgfId-1035096

                # Values:
                # columns
                # rows
                # bit depth (1 or 8)
                # mode (1: L, 2: LAB, 3: RGB, 4: CMYK)
                # number of padding channels
                # block size (number of bytes per row per channel)
                # binary/ascii (1: binary, 2: ascii)
                # data start identifier (the image data follows after a single line
                #   consisting only of this quoted value)
                image_data_values = byte_arr[11:bytes_read].split(None, 7)
                columns, rows, bit_depth, mode_id = (
                    int(value) for value in image_data_values[:4]
                )

                if bit_depth == 1:
                    self._mode = "1"
                elif bit_depth == 8:
                    try:
                        self._mode = self.mode_map[mode_id]
                    except ValueError:
                        break
                else:
                    break

                self._size = columns, rows
                return
            elif trailer_reached and reading_trailer_comments:
                # Load EPS trailer

                # if this line starts with "%%EOF",
                # then we've reached the end of the file
                if bytes_mv[:5] == b"%%EOF":
                    break

                s = str(bytes_mv[:bytes_read], "latin-1")
                _read_comment(s)
            elif bytes_mv[:9] == b"%%Trailer":
                trailer_reached = True
            bytes_read = 0

        check_required_header_comments()

        if not self._size:
            msg = "cannot determine EPS bounding box"
            raise OSError(msg)
