    def skipIFDs(self) -> None:
        while True:
            ifd_offset = self.readLong()
            if ifd_offset == 0:
                self.whereToWriteNewIFDOffset = self.f.tell() - 4
                break

            self.f.seek(ifd_offset)
            num_tags = self.readShort()
            self.f.seek(num_tags * 12, os.SEEK_CUR)
