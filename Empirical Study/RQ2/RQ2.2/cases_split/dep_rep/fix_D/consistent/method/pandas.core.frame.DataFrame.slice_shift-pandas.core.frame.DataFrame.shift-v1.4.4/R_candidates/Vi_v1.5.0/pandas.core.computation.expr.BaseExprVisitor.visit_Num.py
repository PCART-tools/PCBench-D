    def visit_Num(self, node, **kwargs) -> Term:
        return self.const_type(node.n, self.env)
