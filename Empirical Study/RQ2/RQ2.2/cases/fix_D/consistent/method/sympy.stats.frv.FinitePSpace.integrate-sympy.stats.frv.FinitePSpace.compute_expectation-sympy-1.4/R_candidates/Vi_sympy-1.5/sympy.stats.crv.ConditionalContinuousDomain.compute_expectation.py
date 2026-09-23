    def compute_expectation(self, expr, variables=None, **kwargs):
        if variables is None:
            variables = self.symbols
        if not variables:
            return expr
        # Extract the full integral
        fullintgrl = self.fulldomain.compute_expectation(expr, variables)
        # separate into integrand and limits
        integrand, limits = fullintgrl.function, list(fullintgrl.limits)

        conditions = [self.condition]
        while conditions:
            cond = conditions.pop()
            if cond.is_Boolean:
                if isinstance(cond, And):
                    conditions.extend(cond.args)
                elif isinstance(cond, Or):
                    raise NotImplementedError("Or not implemented here")
            elif cond.is_Relational:
                if cond.is_Equality:
                    # Add the appropriate Delta to the integrand
                    integrand *= DiracDelta(cond.lhs - cond.rhs)
                else:
                    symbols = cond.free_symbols & set(self.symbols)
                    if len(symbols) != 1:  # Can't handle x > y
                        raise NotImplementedError(
                            "Multivariate Inequalities not yet implemented")
                    # Can handle x > 0
                    symbol = symbols.pop()
                    # Find the limit with x, such as (x, -oo, oo)
                    for i, limit in enumerate(limits):
                        if limit[0] == symbol:
                            # Make condition into an Interval like [0, oo]
                            cintvl = reduce_rational_inequalities_wrap(
                                cond, symbol)
                            # Make limit into an Interval like [-oo, oo]
                            lintvl = Interval(limit[1], limit[2])
                            # Intersect them to get [0, oo]
                            intvl = cintvl.intersect(lintvl)
                            # Put back into limits list
                            limits[i] = (symbol, intvl.left, intvl.right)
            else:
                raise TypeError(
                    "Condition %s is not a relational or Boolean" % cond)

        return Integral(integrand, *limits, **kwargs)
