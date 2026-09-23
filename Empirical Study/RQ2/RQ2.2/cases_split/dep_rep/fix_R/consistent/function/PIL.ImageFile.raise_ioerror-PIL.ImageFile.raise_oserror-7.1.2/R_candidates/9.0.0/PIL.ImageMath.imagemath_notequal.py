def imagemath_notequal(self, other):
    return self.apply("ne", self, other, mode="I")
