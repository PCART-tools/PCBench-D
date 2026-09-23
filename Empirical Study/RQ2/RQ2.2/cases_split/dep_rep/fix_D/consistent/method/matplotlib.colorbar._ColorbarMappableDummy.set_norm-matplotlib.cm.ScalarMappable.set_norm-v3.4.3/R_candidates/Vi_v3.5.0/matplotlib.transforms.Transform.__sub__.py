    def __sub__(self, other):
        """
        Compose *self* with the inverse of *other*, cancelling identical terms
        if any::

            # In general:
            A - B == A + B.inverted()
            # (but see note regarding frozen transforms below).

            # If A "ends with" B (i.e. A == A' + B for some A') we can cancel
            # out B:
            (A' + B) - B == A'

            # Likewise, if B "starts with" A (B = A + B'), we can cancel out A:
            A - (A + B') == B'.inverted() == B'^-1

        Cancellation (rather than naively returning ``A + B.inverted()``) is
        important for multiple reasons:

        - It avoids floating-point inaccuracies when computing the inverse of
          B: ``B - B`` is guaranteed to cancel out exactly (resulting in the
          identity transform), whereas ``B + B.inverted()`` may differ by a
          small epsilon.
        - ``B.inverted()`` always returns a frozen transform: if one computes
          ``A + B + B.inverted()`` and later mutates ``B``, then
          ``B.inverted()`` won't be updated and the last two terms won't cancel
          out anymore; on the other hand, ``A + B - B`` will always be equal to
          ``A`` even if ``B`` is mutated.
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
