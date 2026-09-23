    def __sub__(self, other):
        """
        Returns a transform stack which goes all the way down self's transform
        stack, and then ascends back up other's stack. If it can, this is
        optimised::

            # normally
            A - B == a + b.inverted()

            # sometimes, when A contains the tree B there is no need to
            # descend all the way down to the base of A (via B), instead we
            # can just stop at B.

            (A + B) - (B)^-1 == A

            # similarly, when B contains tree A, we can avoid descending A at
            # all, basically:
            A - (A + B) == ((B + A) - A).inverted() or B^-1

        For clarity, the result of ``(A + B) - B + B == (A + B)``.

        """
        # we only know how to do this operation if other is a Transform.
        if not isinstance(other, Transform):
            return NotImplemented

        for remainder, sub_tree in self._iter_break_from_left_to_right():
            if sub_tree == other:
                return remainder

        for remainder, sub_tree in other._iter_break_from_left_to_right():
            if sub_tree == self:
                if not remainder.has_inverse:
                    raise ValueError(
                        "The shortcut cannot be computed since 'other' "
                        "includes a non-invertible component")
                return remainder.inverted()

        # if we have got this far, then there was no shortcut possible
        if other.has_inverse:
            return self + other.inverted()
        else:
            raise ValueError('It is not possible to compute transA - transB '
                             'since transB cannot be inverted and there is no '
                             'shortcut possible.')
