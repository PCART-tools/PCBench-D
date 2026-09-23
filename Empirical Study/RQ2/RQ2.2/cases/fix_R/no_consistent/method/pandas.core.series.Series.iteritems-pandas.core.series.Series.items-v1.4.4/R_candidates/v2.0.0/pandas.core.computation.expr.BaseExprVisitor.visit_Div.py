    def visit_Div(self, node, **kwargs):
        return lambda lhs, rhs: Div(lhs, rhs)
