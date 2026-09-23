    def _invalidate_internal(self, value, invalidating_node):
        # In some cases for a composite transform, an invalidating call to
        # AFFINE_ONLY needs to be extended to invalidate the NON_AFFINE part
        # too. These cases are when the right hand transform is non-affine and
        # either:
        # (a) the left hand transform is non affine
        # (b) it is the left hand node which has triggered the invalidation
        if (value == Transform.INVALID_AFFINE and
                not self._b.is_affine and
                (not self._a.is_affine or invalidating_node is self._a)):
            value = Transform.INVALID

        super()._invalidate_internal(value=value,
                                     invalidating_node=invalidating_node)
