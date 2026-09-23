    def visit_Index(self, node, **kwargs):
        return self.visit(node.value).value
