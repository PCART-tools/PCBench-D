    def visit_Div(self, node, **kwargs):
        truediv = self.env.scope['truediv']
        return lambda lhs, rhs: Div(lhs, rhs, truediv)
