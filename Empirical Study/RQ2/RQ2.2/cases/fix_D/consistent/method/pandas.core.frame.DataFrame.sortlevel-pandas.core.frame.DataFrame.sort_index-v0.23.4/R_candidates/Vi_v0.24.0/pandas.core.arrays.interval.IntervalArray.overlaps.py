    @Appender(_interval_shared_docs['overlaps'] % _shared_docs_kwargs)
    def overlaps(self, other):
        if isinstance(other, (IntervalArray, ABCIntervalIndex)):
            raise NotImplementedError
        elif not isinstance(other, Interval):
            msg = '`other` must be Interval-like, got {other}'
            raise TypeError(msg.format(other=type(other).__name__))

        # equality is okay if both endpoints are closed (overlap at a point)
        op1 = le if (self.closed_left and other.closed_right) else lt
        op2 = le if (other.closed_left and self.closed_right) else lt

        # overlaps is equivalent negation of two interval being disjoint:
        # disjoint = (A.left > B.right) or (B.left > A.right)
        # (simplifying the negation allows this to be done in less operations)
        return op1(self.left, other.right) & op2(other.left, self.right)
