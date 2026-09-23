    def visit_Name(self, node, **kwargs):
        return self.term_type(node.id, self.env, **kwargs)
