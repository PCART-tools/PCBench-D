    @classmethod
    def _add_logical_methods_disabled(cls):
        """
        Add in logical methods to disable.
        """
        cls.all = make_invalid_op('all')
        cls.any = make_invalid_op('any')
