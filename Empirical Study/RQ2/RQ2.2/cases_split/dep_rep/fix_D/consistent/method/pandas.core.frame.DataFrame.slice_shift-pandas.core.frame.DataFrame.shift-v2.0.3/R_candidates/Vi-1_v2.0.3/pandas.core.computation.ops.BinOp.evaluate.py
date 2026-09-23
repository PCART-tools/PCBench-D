    def evaluate(self, env, engine: str, parser, term_type, eval_in_python):
        """
        Evaluate a binary operation *before* being passed to the engine.

        Parameters
        ----------
        env : Scope
        engine : str
        parser : str
        term_type : type
        eval_in_python : list

        Returns
        -------
        term_type
            The "pre-evaluated" expression as an instance of ``term_type``
        """
        if engine == "python":
            res = self(env)
        else:
            # recurse over the left/right nodes

            left = self.lhs.evaluate(
                env,
                engine=engine,
                parser=parser,
                term_type=term_type,
                eval_in_python=eval_in_python,
            )

            right = self.rhs.evaluate(
                env,
                engine=engine,
                parser=parser,
                term_type=term_type,
                eval_in_python=eval_in_python,
            )

            # base cases
            if self.op in eval_in_python:
                res = self.func(left.value, right.value)
            else:
                from pandas.core.computation.eval import eval

                res = eval(self, local_dict=env, engine=engine, parser=parser)

        name = env.add_tmp(res)
        return term_type(name, env=env)
