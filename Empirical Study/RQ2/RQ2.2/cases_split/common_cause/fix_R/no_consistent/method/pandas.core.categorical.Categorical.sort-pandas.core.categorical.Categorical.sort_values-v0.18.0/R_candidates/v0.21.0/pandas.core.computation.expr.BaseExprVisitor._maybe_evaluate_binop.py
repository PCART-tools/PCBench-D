    def _maybe_evaluate_binop(self, op, op_class, lhs, rhs,
                              eval_in_python=('in', 'not in'),
                              maybe_eval_in_python=('==', '!=', '<', '>',
                                                    '<=', '>=')):
        res = op(lhs, rhs)

        if res.has_invalid_return_type:
            raise TypeError("unsupported operand type(s) for {op}:"
                            " '{lhs}' and '{rhs}'".format(op=res.op,
                                                          lhs=lhs.type,
                                                          rhs=rhs.type))

        if self.engine != 'pytables':
            if (res.op in _cmp_ops_syms and
                    getattr(lhs, 'is_datetime', False) or
                    getattr(rhs, 'is_datetime', False)):
                # all date ops must be done in python bc numexpr doesn't work
                # well with NaT
                return self._maybe_eval(res, self.binary_ops)

        if res.op in eval_in_python:
            # "in"/"not in" ops are always evaluated in python
            return self._maybe_eval(res, eval_in_python)
        elif self.engine != 'pytables':
            if (getattr(lhs, 'return_type', None) == object or
                    getattr(rhs, 'return_type', None) == object):
                # evaluate "==" and "!=" in python if either of our operands
                # has an object return type
                return self._maybe_eval(res, eval_in_python +
                                        maybe_eval_in_python)
        return res
