    def visit(self, node, **kwargs):
        if isinstance(node, string_types):
            clean = self.preparser(node)
            node = ast.fix_missing_locations(ast.parse(clean))

        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method)
        return visitor(node, **kwargs)
