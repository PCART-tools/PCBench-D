    def __add__(self, other: ImagePointTransform | float) -> ImagePointTransform:
        if isinstance(other, ImagePointTransform):
            return ImagePointTransform(
                self.scale + other.scale, self.offset + other.offset
            )
        return ImagePointTransform(self.scale, self.offset + other)
