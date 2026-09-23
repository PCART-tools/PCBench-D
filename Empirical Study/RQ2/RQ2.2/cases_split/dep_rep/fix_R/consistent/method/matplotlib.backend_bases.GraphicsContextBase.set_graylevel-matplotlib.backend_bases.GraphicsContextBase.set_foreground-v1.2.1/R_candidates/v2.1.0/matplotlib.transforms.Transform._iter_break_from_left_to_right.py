    def _iter_break_from_left_to_right(self):
        """
        Returns an iterator breaking down this transform stack from left to
        right recursively. If self == ((A, N), A) then the result will be an
        iterator which yields I : ((A, N), A), followed by A : (N, A),
        followed by (A, N) : (A), but not ((A, N), A) : I.

        This is equivalent to flattening the stack then yielding
        ``flat_stack[:i], flat_stack[i:]`` where i=0..(n-1).

        """
        yield IdentityTransform(), self
