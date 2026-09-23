    def _open(self):
        read = self.fp.read

        #
        # header

        s = read(26)
        if not _accept(s) or i16(s, 4) != 1:
            msg = "not a PSD file"
            raise SyntaxError(msg)

        psd_bits = i16(s, 22)
        psd_channels = i16(s, 12)
        psd_mode = i16(s, 24)

        mode, channels = MODES[(psd_mode, psd_bits)]

        if channels > psd_channels:
            msg = "not enough channels"
            raise OSError(msg)
        if mode == "RGB" and psd_channels == 4:
            mode = "RGBA"
            channels = 4

        self._mode = mode
        self._size = i32(s, 18), i32(s, 14)

        #
        # color mode data

        size = i32(read(4))
        if size:
            data = read(size)
            if mode == "P" and size == 768:
                self.palette = ImagePalette.raw("RGB;L", data)

        #
        # image resources

        self.resources = []

        size = i32(read(4))
        if size:
            # load resources
            end = self.fp.tell() + size
            while self.fp.tell() < end:
                read(4)  # signature
                id = i16(read(2))
                name = read(i8(read(1)))
                if not (len(name) & 1):
                    read(1)  # padding
                data = read(i32(read(4)))
                if len(data) & 1:
                    read(1)  # padding
                self.resources.append((id, name, data))
                if id == 1039:  # ICC profile
                    self.info["icc_profile"] = data

        #
        # layer and mask information

        self.layers = []

        size = i32(read(4))
        if size:
            end = self.fp.tell() + size
            size = i32(read(4))
            if size:
                _layer_data = io.BytesIO(ImageFile._safe_read(self.fp, size))
                self.layers = _layerinfo(_layer_data, size)
            self.fp.seek(end)
        self.n_frames = len(self.layers)
        self.is_animated = self.n_frames > 1

        #
        # image descriptor

        self.tile = _maketile(self.fp, mode, (0, 0) + self.size, channels)

        # keep the file open
        self._fp = self.fp
        self.frame = 1
        self._min_frame = 1
