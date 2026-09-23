    def __call__(self, env):
        """Recursively evaluate an expression in Python space.

        Parameters
        ----------
        env : Scope

        Returns
        -------
        object
            The result of an evaluated expression.
        """
        # handle truediv
        if self.op == "/" and env.scope["truediv"]:
            self.func = op.truediv

        # recurse over the left/right nodes
        left = self.lhs(env)
        right = self.rhs(env)

        return self.func(left, right)
