    def __inv__(self):
        # TODO: why not operator.inv?
        # TODO: __inv__ vs __invert__?
        return self._unary_method(lambda x: -x)
