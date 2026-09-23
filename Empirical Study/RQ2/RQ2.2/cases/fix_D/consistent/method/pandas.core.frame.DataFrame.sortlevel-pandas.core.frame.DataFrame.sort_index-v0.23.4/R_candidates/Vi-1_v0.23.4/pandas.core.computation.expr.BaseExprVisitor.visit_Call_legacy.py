    def visit_Call_legacy(self, node, side=None, **kwargs):

        # this can happen with: datetime.datetime
        if isinstance(node.func, ast.Attribute):
            res = self.visit_Attribute(node.func)
        elif not isinstance(node.func, ast.Name):
            raise TypeError("Only named functions are supported")
        else:
            try:
                res = self.visit(node.func)
            except UndefinedVariableError:
                # Check if this is a supported function name
                try:
                    res = FuncNode(node.func.id)
                except ValueError:
                    # Raise original error
                    raise

        if res is None:
            raise ValueError("Invalid function call {func}"
                             .format(func=node.func.id))
        if hasattr(res, 'value'):
            res = res.value

        if isinstance(res, FuncNode):
            args = [self.visit(targ) for targ in node.args]

            if node.starargs is not None:
                args += self.visit(node.starargs)

            if node.keywords or node.kwargs:
                raise TypeError("Function \"{name}\" does not support keyword "
                                "arguments".format(name=res.name))

            return res(*args, **kwargs)

        else:
            args = [self.visit(targ).value for targ in node.args]
            if node.starargs is not None:
                args += self.visit(node.starargs).value

            keywords = {}
            for key in node.keywords:
                if not isinstance(key, ast.keyword):
                    raise ValueError("keyword error in function call "
                                     "'{func}'".format(func=node.func.id))
                keywords[key.arg] = self.visit(key.value).value
            if node.kwargs is not None:
                keywords.update(self.visit(node.kwargs).value)

            return self.const_type(res(*args, **keywords), self.env)
