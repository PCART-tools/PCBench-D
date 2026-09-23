    def visit_Num(self, node, **kwargs):
        return self.const_type(node.n, self.env)
