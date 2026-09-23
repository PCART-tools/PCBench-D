    def visit_Index(self, node, **kwargs):
        """ df.index[4] """
        return self.visit(node.value)
