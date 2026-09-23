    def _open(self) -> None:
        """Open the first image in a TIFF file"""

        # Header
        ifh = self.fp.read(8)
        if ifh[2] == 43:
            ifh += self.fp.read(8)

        self.tag_v2 = ImageFileDirectory_v2(ifh)

        # legacy IFD entries will be filled in later
        self.ifd = None

        # setup frame pointers
        self.__first = self.__next = self.tag_v2.next
        self.__frame = -1
        self._fp = self.fp
        self._frame_pos: list[int] = []
        self._n_frames: int | None = None

        logger.debug("*** TiffImageFile._open ***")
        logger.debug("- __first: %s", self.__first)
        logger.debug("- ifh: %s", repr(ifh))  # Use repr to avoid str(bytes)

        # and load the first frame
        self._seek(0)
