    @staticmethod
    @_api.deprecated("3.6", alternative="Affine2D()")
    def identity():
        """
        Return a new `Affine2D` object that is the identity transform.

        Unless this transform will be mutated later on, consider using
        the faster `IdentityTransform` class instead.
        """
        return Affine2D()
