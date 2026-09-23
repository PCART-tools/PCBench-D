    def visit_NameConstant(self, node, **kwargs):
        return self.const_type(node.value, self.env)
