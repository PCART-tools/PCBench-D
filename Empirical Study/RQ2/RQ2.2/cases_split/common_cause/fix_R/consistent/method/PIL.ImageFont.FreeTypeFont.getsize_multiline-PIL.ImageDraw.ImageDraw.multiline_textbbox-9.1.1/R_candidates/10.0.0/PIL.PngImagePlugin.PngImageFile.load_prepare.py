    def load_prepare(self):
        """internal: prepare to read PNG file"""

        if self.info.get("interlace"):
            self.decoderconfig = self.decoderconfig + (1,)

        self.__idat = self.__prepare_idat  # used by load_read()
        ImageFile.ImageFile.load_prepare(self)
