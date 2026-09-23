def _cat_compare_op(op):
    def f(self, other):
        # On python2, you can usually compare any type to any type, and
        # Categoricals can be seen as a custom type, but having different
        # results depending whether categories are the same or not is kind of
        # insane, so be a bit stricter here and use the python3 idea of
        # comparing only things of equal type.
        if not self.ordered:
            if op in ['__lt__', '__gt__', '__le__', '__ge__']:
                raise TypeError("Unordered Categoricals can only compare "
                                "equality or not")
        if isinstance(other, Categorical):
            # Two Categoricals can only be be compared if the categories are
            # the same
            if ((len(self.categories) != len(other.categories)) or
                    not ((self.categories == other.categories).all())):
                raise TypeError("Categoricals can only be compared if "
                                "'categories' are the same")
            if not (self.ordered == other.ordered):
                raise TypeError("Categoricals can only be compared if "
                                "'ordered' is the same")
            na_mask = (self._codes == -1) | (other._codes == -1)
            f = getattr(self._codes, op)
            ret = f(other._codes)
            if na_mask.any():
                # In other series, the leads to False, so do that here too
                ret[na_mask] = False
            return ret

        # Numpy-1.9 and earlier may convert a scalar to a zerodim array during
        # comparison operation when second arg has higher priority, e.g.
        #
        #     cat[0] < cat
        #
        # With cat[0], for example, being ``np.int64(1)`` by the time it gets
        # into this function would become ``np.array(1)``.
        other = lib.item_from_zerodim(other)
        if is_scalar(other):
            if other in self.categories:
                i = self.categories.get_loc(other)
                return getattr(self._codes, op)(i)
            else:
                if op == '__eq__':
                    return np.repeat(False, len(self))
                elif op == '__ne__':
                    return np.repeat(True, len(self))
                else:
                    msg = ("Cannot compare a Categorical for op {op} with a "
                           "scalar, which is not a category.")
                    raise TypeError(msg.format(op=op))
        else:

            # allow categorical vs object dtype array comparisons for equality
            # these are only positional comparisons
            if op in ['__eq__', '__ne__']:
                return getattr(np.array(self), op)(np.array(other))

            msg = ("Cannot compare a Categorical for op {op} with type {typ}."
                   "\nIf you want to compare values, use 'np.asarray(cat) "
                   "<op> other'.")
            raise TypeError(msg.format(op=op, typ=type(other)))

    f.__name__ = op

    return f
