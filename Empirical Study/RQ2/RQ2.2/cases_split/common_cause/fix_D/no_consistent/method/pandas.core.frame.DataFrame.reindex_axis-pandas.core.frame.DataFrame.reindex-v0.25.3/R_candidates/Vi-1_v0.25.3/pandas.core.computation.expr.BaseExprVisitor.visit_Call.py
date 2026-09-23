    def visit_Call(self, node, side=None, **kwargs):

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
            raise ValueError("Invalid function call {func}".format(func=node.func.id))
        if hasattr(res, "value"):
            res = res.value

        if isinstance(res, FuncNode):

            new_args = [self.visit(arg) for arg in node.args]

            if node.keywords:
                raise TypeError(
                    'Function "{name}" does not support keyword '
                    "arguments".format(name=res.name)
                )

            return res(*new_args, **kwargs)

        else:

            new_args = [self.visit(arg).value for arg in node.args]

            for key in node.keywords:
                if not isinstance(key, ast.keyword):
                    raise ValueError(
                        "keyword error in function call "
                        "'{func}'".format(func=node.func.id)
                    )

                if key.arg:
                    kwargs[key.arg] = self.visit(key.value).value

            return self.const_type(res(*new_args, **kwargs), self.env)
