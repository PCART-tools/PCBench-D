    def visit_Subscript(self, node, **kwargs):
        # only allow simple suscripts

        value = self.visit(node.value)
        slobj = self.visit(node.slice)
        try:
            value = value.value
        except AttributeError:
            pass

        try:
            return self.const_type(value[slobj], self.env)
        except TypeError:
            raise ValueError("cannot subscript {value!r} with "
                             "{slobj!r}".format(value=value, slobj=slobj))
