    def _seek(self, frame):
        self.fp = self._fp

        # reset buffered io handle in case fp
        # was passed to libtiff, invalidating the buffer
        self.fp.tell()

        while len(self._frame_pos) <= frame:
            if not self.__next:
                msg = "no more images in TIFF file"
                raise EOFError(msg)
            logger.debug(
                f"Seeking to frame {frame}, on frame {self.__frame}, "
                f"__next {self.__next}, location: {self.fp.tell()}"
            )
            self.fp.seek(self.__next)
            self._frame_pos.append(self.__next)
            logger.debug("Loading tags, location: %s" % self.fp.tell())
            self.tag_v2.load(self.fp)
            if self.tag_v2.next in self._frame_pos:
                # This IFD has already been processed
                # Declare this to be the end of the image
                self.__next = 0
            else:
                self.__next = self.tag_v2.next
            if self.__next == 0:
                self._n_frames = frame + 1
            if len(self._frame_pos) == 1:
                self.is_animated = self.__next != 0
            self.__frame += 1
        self.fp.seek(self._frame_pos[frame])
        self.tag_v2.load(self.fp)
        self._reload_exif()
        # fill the legacy tag/ifd entries
        self.tag = self.ifd = ImageFileDirectory_v1.from_v2(self.tag_v2)
        self.__frame = frame
        self._setup()
