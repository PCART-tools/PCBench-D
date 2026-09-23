    @classmethod
    def _add_numericlike_set_methods_disabled(cls):
        """ add in the numeric set-like methods to disable """

        def _make_invalid_op(name):

            def invalid_op(self, other=None):
                raise TypeError("cannot perform {name} with this index type: {typ}".format(name=name,
                                                                                           typ=type(self)))
            invalid_op.__name__ = name
            return invalid_op

        cls.__add__ = cls.__radd__ = __iadd__ = _make_invalid_op('__add__')
        cls.__sub__ = __isub__ = _make_invalid_op('__sub__')
