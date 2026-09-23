    def visit_Expr(self, node, **kwargs):
        return self.visit(node.value, **kwargs)
