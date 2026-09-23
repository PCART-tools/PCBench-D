    def _make_deprecated_unary(op, name):
        # op is a callable

        def _evaluate_numeric_unary(self):
            result = self._deprecated(name)
            return op(result)
        return _evaluate_numeric_unary
