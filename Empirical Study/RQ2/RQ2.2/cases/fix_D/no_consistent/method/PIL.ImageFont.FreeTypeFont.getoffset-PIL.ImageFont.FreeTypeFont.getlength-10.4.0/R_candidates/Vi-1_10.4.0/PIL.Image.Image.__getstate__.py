    def __getstate__(self):
        im_data = self.tobytes()  # load image first
        return [self.info, self.mode, self.size, self.getpalette(), im_data]
