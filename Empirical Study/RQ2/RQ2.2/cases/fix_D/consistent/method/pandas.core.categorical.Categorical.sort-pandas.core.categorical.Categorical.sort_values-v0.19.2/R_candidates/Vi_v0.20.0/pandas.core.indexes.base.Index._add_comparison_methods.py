    @classmethod
    def _add_comparison_methods(cls):
        """ add in comparison methods """

        def _make_compare(op):
            def _evaluate_compare(self, other):
                if isinstance(other, (np.ndarray, Index, ABCSeries)):
                    if other.ndim > 0 and len(self) != len(other):
                        raise ValueError('Lengths must match to compare')

                # we may need to directly compare underlying
                # representations
                if needs_i8_conversion(self) and needs_i8_conversion(other):
                    return self._evaluate_compare(other, op)

                if (is_object_dtype(self) and
                        self.nlevels == 1):

                    # don't pass MultiIndex
                    with np.errstate(all='ignore'):
                        result = _comp_method_OBJECT_ARRAY(
                            op, self.values, other)
                else:
                    with np.errstate(all='ignore'):
                        result = op(self.values, np.asarray(other))

                # technically we could support bool dtyped Index
                # for now just return the indexing array directly
                if is_bool_dtype(result):
                    return result
                try:
                    return Index(result)
                except TypeError:
                    return result

            return _evaluate_compare

        cls.__eq__ = _make_compare(operator.eq)
        cls.__ne__ = _make_compare(operator.ne)
        cls.__lt__ = _make_compare(operator.lt)
        cls.__gt__ = _make_compare(operator.gt)
        cls.__le__ = _make_compare(operator.le)
        cls.__ge__ = _make_compare(operator.ge)
