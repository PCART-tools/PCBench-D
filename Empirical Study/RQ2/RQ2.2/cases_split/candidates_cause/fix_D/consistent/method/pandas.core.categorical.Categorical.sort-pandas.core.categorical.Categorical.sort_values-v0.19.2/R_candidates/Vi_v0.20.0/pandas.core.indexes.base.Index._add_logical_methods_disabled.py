    @classmethod
    def _add_logical_methods_disabled(cls):
        """ add in logical methods to disable """

        def _make_invalid_op(name):
            def invalid_op(self, other=None):
                raise TypeError("cannot perform {name} with this index type: "
                                "{typ}".format(name=name, typ=type(self)))

            invalid_op.__name__ = name
            return invalid_op

        cls.all = _make_invalid_op('all')
        cls.any = _make_invalid_op('any')
