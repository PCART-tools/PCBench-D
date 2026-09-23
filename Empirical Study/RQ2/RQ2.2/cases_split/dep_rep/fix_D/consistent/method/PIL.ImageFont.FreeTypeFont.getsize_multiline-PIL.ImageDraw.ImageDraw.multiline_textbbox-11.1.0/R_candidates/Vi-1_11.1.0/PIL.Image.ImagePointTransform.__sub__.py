    def __sub__(self, other: ImagePointTransform | float) -> ImagePointTransform:
        return self + -other
