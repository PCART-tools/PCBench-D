    def _open(self) -> None:
        # load descriptive fields
        while True:
            offset = self.fp.tell()
            tag, size = self.field()
            if not tag or tag == (8, 10):
                break
            if size:
                tagdata = self.fp.read(size)
            else:
                tagdata = None
            if tag in self.info:
                if isinstance(self.info[tag], list):
                    self.info[tag].append(tagdata)
                else:
                    self.info[tag] = [self.info[tag], tagdata]
            else:
                self.info[tag] = tagdata

        # mode
        layers = self.info[(3, 60)][0]
        component = self.info[(3, 60)][1]
        if (3, 65) in self.info:
            id = self.info[(3, 65)][0] - 1
        else:
            id = 0
        if layers == 1 and not component:
            self._mode = "L"
        elif layers == 3 and component:
            self._mode = "RGB"[id]
        elif layers == 4 and component:
            self._mode = "CMYK"[id]

        # size
        self._size = self.getint((3, 20)), self.getint((3, 30))

        # compression
        try:
            compression = COMPRESSION[self.getint((3, 120))]
        except KeyError as e:
            msg = "Unknown IPTC image compression"
            raise OSError(msg) from e

        # tile
        if tag == (8, 10):
            self.tile = [("iptc", (0, 0) + self.size, offset, compression)]
