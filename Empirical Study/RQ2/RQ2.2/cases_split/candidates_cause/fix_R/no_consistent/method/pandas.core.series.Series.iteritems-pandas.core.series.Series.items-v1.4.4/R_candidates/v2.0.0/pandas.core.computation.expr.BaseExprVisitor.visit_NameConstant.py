    def visit_NameConstant(self, node, **kwargs) -> Term:
        return self.const_type(node.value, self.env)
