    def visit_Constant(self, node, **kwargs):
        return self.const_type(node.n, self.env)
