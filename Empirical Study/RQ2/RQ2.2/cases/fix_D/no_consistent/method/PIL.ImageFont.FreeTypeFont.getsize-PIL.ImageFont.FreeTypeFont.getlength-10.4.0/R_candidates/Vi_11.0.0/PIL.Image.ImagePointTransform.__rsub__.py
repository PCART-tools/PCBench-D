    def __rsub__(self, other: ImagePointTransform | float) -> ImagePointTransform:
        return other + -self
