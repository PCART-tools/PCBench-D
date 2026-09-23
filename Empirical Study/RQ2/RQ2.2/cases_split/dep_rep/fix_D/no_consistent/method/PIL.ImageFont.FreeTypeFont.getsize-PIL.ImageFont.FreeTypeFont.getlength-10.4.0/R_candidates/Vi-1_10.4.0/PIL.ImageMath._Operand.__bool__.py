    def __bool__(self) -> bool:
        # an image is "true" if it contains at least one non-zero pixel
        return self.im.getbbox() is not None
