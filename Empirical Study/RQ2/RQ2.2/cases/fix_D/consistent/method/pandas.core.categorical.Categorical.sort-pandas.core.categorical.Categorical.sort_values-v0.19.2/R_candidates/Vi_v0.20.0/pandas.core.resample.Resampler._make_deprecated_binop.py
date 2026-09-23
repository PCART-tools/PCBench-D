    def _make_deprecated_binop(op):
        # op is a string

        def _evaluate_numeric_binop(self, other):
            result = self._deprecated(op)
            return getattr(result, op)(other)
        return _evaluate_numeric_binop
