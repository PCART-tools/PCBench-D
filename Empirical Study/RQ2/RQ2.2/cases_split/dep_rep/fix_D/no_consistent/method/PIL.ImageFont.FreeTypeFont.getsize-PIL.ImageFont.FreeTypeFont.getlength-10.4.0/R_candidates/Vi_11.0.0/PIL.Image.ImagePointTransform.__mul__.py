    def __mul__(self, other: ImagePointTransform | float) -> ImagePointTransform:
        if isinstance(other, ImagePointTransform):
            return NotImplemented
        return ImagePointTransform(self.scale * other, self.offset * other)
