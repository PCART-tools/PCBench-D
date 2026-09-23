    def __neg__(self) -> ImagePointTransform:
        return ImagePointTransform(-self.scale, -self.offset)
