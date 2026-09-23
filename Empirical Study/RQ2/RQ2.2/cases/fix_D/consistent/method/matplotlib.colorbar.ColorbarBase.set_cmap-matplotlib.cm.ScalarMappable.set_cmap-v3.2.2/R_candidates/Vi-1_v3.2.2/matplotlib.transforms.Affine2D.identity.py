    @staticmethod
    def identity():
        """
        Return a new `Affine2D` object that is the identity transform.

        Unless this transform will be mutated later on, consider using
        the faster :class:`IdentityTransform` class instead.
        """
        return Affine2D()
