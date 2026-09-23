    def visit_Subscript(self, node, **kwargs):
        # only allow simple subscripts

        value = self.visit(node.value)
        slobj = self.visit(node.slice)
        try:
            value = value.value
        except AttributeError:
            pass

        if isinstance(slobj, Term):
            # In py39 np.ndarray lookups with Term containing int raise
            slobj = slobj.value

        try:
            return self.const_type(value[slobj], self.env)
        except TypeError as err:
            raise ValueError(
                f"cannot subscript {repr(value)} with {repr(slobj)}"
            ) from err
