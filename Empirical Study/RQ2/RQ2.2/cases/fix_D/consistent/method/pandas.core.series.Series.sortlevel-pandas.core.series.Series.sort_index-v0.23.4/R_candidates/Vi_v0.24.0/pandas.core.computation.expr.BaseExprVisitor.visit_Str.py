    def visit_Str(self, node, **kwargs):
        name = self.env.add_tmp(node.s)
        return self.term_type(name, self.env)
