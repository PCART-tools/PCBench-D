    def translate_In(self, op):
        return ast.Eq() if isinstance(op, ast.In) else op
