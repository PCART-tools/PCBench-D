    def __bool__(self):
        # an image is "true" if it contains at least one non-zero pixel
        return self.im.getbbox() is not None
