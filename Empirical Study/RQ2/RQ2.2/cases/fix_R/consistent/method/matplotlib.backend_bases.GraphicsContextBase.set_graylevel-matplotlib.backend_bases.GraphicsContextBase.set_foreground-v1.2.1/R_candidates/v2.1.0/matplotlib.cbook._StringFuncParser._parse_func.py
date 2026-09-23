    def _parse_func(self):
        """
        Parses the parameters to build a new _FuncInfo object,
        replacing the relevant parameters if necessary in the lambda
        functions.

        """

        func = self._funcs[self._key]

        if not self._params:
            func = _FuncInfo(func.function, func.inverse,
                             func.is_bounded_0_1())
        else:
            m = func.function
            function = (lambda x, m=m: m(x, self._params))

            m = func.inverse
            inverse = (lambda x, m=m: m(x, self._params))

            is_bounded_0_1 = func.is_bounded_0_1(self._params)

            func = _FuncInfo(function, inverse,
                             is_bounded_0_1)
        return func
