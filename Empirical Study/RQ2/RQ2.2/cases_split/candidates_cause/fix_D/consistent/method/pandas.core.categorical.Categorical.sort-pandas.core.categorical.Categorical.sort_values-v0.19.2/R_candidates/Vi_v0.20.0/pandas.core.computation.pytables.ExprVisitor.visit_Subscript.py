    def visit_Subscript(self, node, **kwargs):
        # only allow simple suscripts

        value = self.visit(node.value)
        slobj = self.visit(node.slice)
        try:
            value = value.value
        except:
            pass

        try:
            return self.const_type(value[slobj], self.env)
        except TypeError:
            raise ValueError("cannot subscript {0!r} with "
                             "{1!r}".format(value, slobj))
