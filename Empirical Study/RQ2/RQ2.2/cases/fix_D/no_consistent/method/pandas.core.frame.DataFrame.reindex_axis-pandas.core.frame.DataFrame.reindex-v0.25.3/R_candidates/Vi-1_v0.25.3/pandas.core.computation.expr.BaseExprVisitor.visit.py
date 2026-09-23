    def visit(self, node, **kwargs):
        if isinstance(node, str):
            clean = self.preparser(node)
            try:
                node = ast.fix_missing_locations(ast.parse(clean))
            except SyntaxError as e:
                from keyword import iskeyword

                if any(iskeyword(x) for x in clean.split()):
                    e.msg = "Python keyword not valid identifier" " in numexpr query"
                raise e

        method = "visit_" + node.__class__.__name__
        visitor = getattr(self, method)
        return visitor(node, **kwargs)
