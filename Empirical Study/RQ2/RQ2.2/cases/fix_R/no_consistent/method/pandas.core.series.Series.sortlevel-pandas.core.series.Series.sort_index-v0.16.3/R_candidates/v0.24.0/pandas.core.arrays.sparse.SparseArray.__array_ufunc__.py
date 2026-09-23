    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get('out', ())

        for x in inputs + out:
            if not isinstance(x, self._HANDLED_TYPES + (SparseArray,)):
                return NotImplemented

        special = {'add', 'sub', 'mul', 'pow', 'mod', 'floordiv', 'truediv',
                   'divmod', 'eq', 'ne', 'lt', 'gt', 'le', 'ge', 'remainder'}
        if compat.PY2:
            special.add('div')
        aliases = {
            'subtract': 'sub',
            'multiply': 'mul',
            'floor_divide': 'floordiv',
            'true_divide': 'truediv',
            'power': 'pow',
            'remainder': 'mod',
            'divide': 'div',
            'equal': 'eq',
            'not_equal': 'ne',
            'less': 'lt',
            'less_equal': 'le',
            'greater': 'gt',
            'greater_equal': 'ge',
        }

        flipped = {
            'lt': '__gt__',
            'le': '__ge__',
            'gt': '__lt__',
            'ge': '__le__',
            'eq': '__eq__',
            'ne': '__ne__',
        }

        op_name = ufunc.__name__
        op_name = aliases.get(op_name, op_name)

        if op_name in special and kwargs.get('out') is None:
            if isinstance(inputs[0], type(self)):
                return getattr(self, '__{}__'.format(op_name))(inputs[1])
            else:
                name = flipped.get(op_name, '__r{}__'.format(op_name))
                return getattr(self, name)(inputs[0])

        if len(inputs) == 1:
            # No alignment necessary.
            sp_values = getattr(ufunc, method)(self.sp_values, **kwargs)
            fill_value = getattr(ufunc, method)(self.fill_value, **kwargs)
            return self._simple_new(sp_values,
                                    self.sp_index,
                                    SparseDtype(sp_values.dtype, fill_value))

        result = getattr(ufunc, method)(*[np.asarray(x) for x in inputs],
                                        **kwargs)
        if out:
            if len(out) == 1:
                out = out[0]
            return out

        if type(result) is tuple:
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            # no return value
            return None
        else:
            return type(self)(result)
