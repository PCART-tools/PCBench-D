    def _open(self):
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
        self._frame_pos = []
        self._n_frames = None

        logger.debug("*** TiffImageFile._open ***")
        logger.debug(f"- __first: {self.__first}")
        logger.debug(f"- ifh: {repr(ifh)}")  # Use repr to avoid str(bytes)

        # and load the first frame
        self._seek(0)
