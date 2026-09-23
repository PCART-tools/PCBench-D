    def _rewrite_membership_op(self, node, left, right):
        return self.visit(node.op), node.op, left, right
