    def visit_Assign(self, node, **kwargs):
        cmpr = ast.Compare(ops=[ast.Eq()], left=node.targets[0],
                           comparators=[node.value])
        return self.visit(cmpr)
