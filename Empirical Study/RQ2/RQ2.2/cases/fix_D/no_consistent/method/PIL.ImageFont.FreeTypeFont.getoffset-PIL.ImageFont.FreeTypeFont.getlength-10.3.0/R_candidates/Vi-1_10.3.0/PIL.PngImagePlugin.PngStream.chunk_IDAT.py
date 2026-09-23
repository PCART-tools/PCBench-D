    def chunk_IDAT(self, pos, length):
        # image data
        if "bbox" in self.im_info:
            tile = [("zip", self.im_info["bbox"], pos, self.im_rawmode)]
        else:
            if self.im_n_frames is not None:
                self.im_info["default_image"] = True
            tile = [("zip", (0, 0) + self.im_size, pos, self.im_rawmode)]
        self.im_tile = tile
        self.im_idat = length
        msg = "image data found"
        raise EOFError(msg)
