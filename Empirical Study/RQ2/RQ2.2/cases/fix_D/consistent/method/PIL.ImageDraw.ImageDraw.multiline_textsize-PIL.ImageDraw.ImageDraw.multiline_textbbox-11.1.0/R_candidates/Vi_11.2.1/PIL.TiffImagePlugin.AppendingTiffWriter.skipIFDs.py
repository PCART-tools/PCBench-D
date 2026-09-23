    def skipIFDs(self) -> None:
        while True:
            ifd_offset = self._read(8 if self._bigtiff else 4)
            if ifd_offset == 0:
                self.whereToWriteNewIFDOffset = self.f.tell() - (
                    8 if self._bigtiff else 4
                )
                break

            self.f.seek(ifd_offset)
            num_tags = self._read(8 if self._bigtiff else 2)
            self.f.seek(num_tags * (20 if self._bigtiff else 12), os.SEEK_CUR)
