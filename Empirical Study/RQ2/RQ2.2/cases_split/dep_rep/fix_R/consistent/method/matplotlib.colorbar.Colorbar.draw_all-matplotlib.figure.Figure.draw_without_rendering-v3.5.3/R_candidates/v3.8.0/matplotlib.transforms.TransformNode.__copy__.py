    def __copy__(self):
        other = copy.copy(super())
        # If `c = a + b; a1 = copy(a)`, then modifications to `a1` do not
        # propagate back to `c`, i.e. we need to clear the parents of `a1`.
        other._parents = {}
        # If `c = a + b; c1 = copy(c)`, then modifications to `a` also need to
        # be propagated to `c1`.
        for key, val in vars(self).items():
            if isinstance(val, TransformNode) and id(self) in val._parents:
                other.set_children(val)  # val == getattr(other, key)
        return other
