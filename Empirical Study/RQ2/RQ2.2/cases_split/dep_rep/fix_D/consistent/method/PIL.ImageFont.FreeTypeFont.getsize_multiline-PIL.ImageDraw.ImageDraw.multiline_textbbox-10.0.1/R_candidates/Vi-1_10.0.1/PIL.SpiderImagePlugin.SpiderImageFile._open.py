    def _open(self):
        # check header
        n = 27 * 4  # read 27 float values
        f = self.fp.read(n)

        try:
            self.bigendian = 1
            t = struct.unpack(">27f", f)  # try big-endian first
            hdrlen = isSpiderHeader(t)
            if hdrlen == 0:
                self.bigendian = 0
                t = struct.unpack("<27f", f)  # little-endian
                hdrlen = isSpiderHeader(t)
            if hdrlen == 0:
                msg = "not a valid Spider file"
                raise SyntaxError(msg)
        except struct.error as e:
            msg = "not a valid Spider file"
            raise SyntaxError(msg) from e

        h = (99,) + t  # add 1 value : spider header index starts at 1
        iform = int(h[5])
        if iform != 1:
            msg = "not a Spider 2D image"
            raise SyntaxError(msg)

        self._size = int(h[12]), int(h[2])  # size in pixels (width, height)
        self.istack = int(h[24])
        self.imgnumber = int(h[27])

        if self.istack == 0 and self.imgnumber == 0:
            # stk=0, img=0: a regular 2D image
            offset = hdrlen
            self._nimages = 1
        elif self.istack > 0 and self.imgnumber == 0:
            # stk>0, img=0: Opening the stack for the first time
            self.imgbytes = int(h[12]) * int(h[2]) * 4
            self.hdrlen = hdrlen
            self._nimages = int(h[26])
            # Point to the first image in the stack
            offset = hdrlen * 2
            self.imgnumber = 1
        elif self.istack == 0 and self.imgnumber > 0:
            # stk=0, img>0: an image within the stack
            offset = hdrlen + self.stkoffset
            self.istack = 2  # So Image knows it's still a stack
        else:
            msg = "inconsistent stack header values"
            raise SyntaxError(msg)

        if self.bigendian:
            self.rawmode = "F;32BF"
        else:
            self.rawmode = "F;32F"
        self.mode = "F"

        self.tile = [("raw", (0, 0) + self.size, offset, (self.rawmode, 0, 1))]
        self._fp = self.fp  # FIXME: hack
