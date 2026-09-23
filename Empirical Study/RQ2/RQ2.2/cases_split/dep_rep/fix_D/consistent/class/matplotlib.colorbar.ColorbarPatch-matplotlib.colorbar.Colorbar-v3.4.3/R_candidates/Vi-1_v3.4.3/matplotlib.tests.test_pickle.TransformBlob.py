class TransformBlob:
    def __init__(self):
        self.identity = mtransforms.IdentityTransform()
        self.identity2 = mtransforms.IdentityTransform()
        # Force use of the more complex composition.
        self.composite = mtransforms.CompositeGenericTransform(
            self.identity,
            self.identity2)
        # Check parent -> child links of TransformWrapper.
        self.wrapper = mtransforms.TransformWrapper(self.composite)
        # Check child -> parent links of TransformWrapper.
        self.composite2 = mtransforms.CompositeGenericTransform(
            self.wrapper,
            self.identity)
