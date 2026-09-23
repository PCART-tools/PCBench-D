    def _evaluate(self):
        import numexpr as ne

        # convert the expression to a valid numexpr expression
        s = self.convert()

        try:
            env = self.expr.env
            scope = env.full_scope
            truediv = scope['truediv']
            _check_ne_builtin_clash(self.expr)
            return ne.evaluate(s, local_dict=scope, truediv=truediv)
        except KeyError as e:
            # python 3 compat kludge
            try:
                msg = e.message
            except AttributeError:
                msg = compat.text_type(e)
            raise UndefinedVariableError(msg)
