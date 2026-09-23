    def visit_Attribute(self, node, **kwargs):
        attr = node.attr
        value = node.value

        ctx = type(node.ctx)
        if ctx == ast.Load:
            # resolve the value
            resolved = self.visit(value)

            # try to get the value to see if we are another expression
            try:
                resolved = resolved.value
            except AttributeError:
                pass

            try:
                return self.term_type(getattr(resolved, attr), self.env)
            except AttributeError:
                # something like datetime.datetime where scope is overridden
                if isinstance(value, ast.Name) and value.id == attr:
                    return resolved

        raise ValueError(f"Invalid Attribute context {ctx.__name__}")
