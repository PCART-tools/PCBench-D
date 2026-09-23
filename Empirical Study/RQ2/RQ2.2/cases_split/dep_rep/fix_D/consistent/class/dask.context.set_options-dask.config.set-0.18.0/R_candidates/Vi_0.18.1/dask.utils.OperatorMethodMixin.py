class OperatorMethodMixin(object):
    """A mixin for dynamically implementing operators"""

    @classmethod
    def _bind_operator(cls, op):
        """ bind operator to this class """
        name = op.__name__

        if name.endswith('_'):
            # for and_ and or_
            name = name[:-1]
        elif name == 'inv':
            name = 'invert'

        meth = '__{0}__'.format(name)

        if name in ('abs', 'invert', 'neg', 'pos'):
            bind_method(cls, meth, cls._get_unary_operator(op))
        else:
            bind_method(cls, meth, cls._get_binary_operator(op))

            if name in ('eq', 'gt', 'ge', 'lt', 'le', 'ne', 'getitem'):
                return

            rmeth = '__r{0}__'.format(name)
            bind_method(cls, rmeth, cls._get_binary_operator(op, inv=True))

    @classmethod
    def _get_unary_operator(cls, op):
        """ Must return a method used by unary operator """
        raise NotImplementedError

    @classmethod
    def _get_binary_operator(cls, op, inv=False):
        """ Must return a method used by binary operator """
        raise NotImplementedError
