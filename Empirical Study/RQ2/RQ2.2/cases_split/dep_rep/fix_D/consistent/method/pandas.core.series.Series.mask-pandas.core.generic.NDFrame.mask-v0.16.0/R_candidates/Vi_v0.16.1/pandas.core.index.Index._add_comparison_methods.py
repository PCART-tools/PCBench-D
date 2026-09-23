    @classmethod
    def _add_comparison_methods(cls):
        """ add in comparison methods """

        def _make_compare(op):

            def _evaluate_compare(self, other):
                func = getattr(self.values, op)
                result = func(np.asarray(other))

                # technically we could support bool dtyped Index
                # for now just return the indexing array directly
                if is_bool_dtype(result):
                    return result
                try:
                    return Index(result)
                except TypeError:
                    return result

            return _evaluate_compare

        cls.__eq__ = _make_compare('__eq__')
        cls.__ne__ = _make_compare('__ne__')
        cls.__lt__ = _make_compare('__lt__')
        cls.__gt__ = _make_compare('__gt__')
        cls.__le__ = _make_compare('__le__')
        cls.__ge__ = _make_compare('__ge__')
