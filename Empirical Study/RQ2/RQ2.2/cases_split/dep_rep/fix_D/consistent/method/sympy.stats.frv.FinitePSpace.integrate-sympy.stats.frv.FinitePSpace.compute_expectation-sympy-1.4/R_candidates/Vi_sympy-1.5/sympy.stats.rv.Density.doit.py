    def doit(self, evaluate=True, **kwargs):
        from sympy.stats.joint_rv import JointPSpace
        from sympy.stats.frv import SingleFiniteDistribution
        expr, condition = self.expr, self.condition
        if _sympify(expr).has(RandomMatrixSymbol):
            return pspace(expr).compute_density(expr)
        if isinstance(expr, SingleFiniteDistribution):
            return expr.dict
        if condition is not None:
            # Recompute on new conditional expr
            expr = given(expr, condition, **kwargs)
        if isinstance(expr, RandomSymbol) and \
            isinstance(expr.pspace, JointPSpace):
            return expr.pspace.distribution
        if not random_symbols(expr):
            return Lambda(x, DiracDelta(x - expr))
        if (isinstance(expr, RandomSymbol) and
            hasattr(expr.pspace, 'distribution') and
            isinstance(pspace(expr), (SinglePSpace))):
            return expr.pspace.distribution
        result = pspace(expr).compute_density(expr, **kwargs)

        if evaluate and hasattr(result, 'doit'):
            return result.doit()
        else:
            return result
