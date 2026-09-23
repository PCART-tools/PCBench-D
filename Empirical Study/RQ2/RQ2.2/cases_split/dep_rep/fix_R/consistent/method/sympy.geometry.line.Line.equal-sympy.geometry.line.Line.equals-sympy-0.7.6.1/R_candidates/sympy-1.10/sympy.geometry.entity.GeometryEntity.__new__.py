    def __new__(cls, *args, **kwargs):
        # Points are sequences, but they should not
        # be converted to Tuples, so use this detection function instead.
        def is_seq_and_not_point(a):
            # we cannot use isinstance(a, Point) since we cannot import Point
            if hasattr(a, 'is_Point') and a.is_Point:
                return False
            return is_sequence(a)

        args = [Tuple(*a) if is_seq_and_not_point(a) else sympify(a) for a in args]
        return Basic.__new__(cls, *args)
