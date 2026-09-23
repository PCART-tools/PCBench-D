    @classmethod
    def _create_arithmetic_method(cls, op):
        def sparse_arithmetic_method(self, other):
            op_name = op.__name__

            if isinstance(other, (ABCSeries, ABCIndexClass)):
                # Rely on pandas to dispatch to us.
                return NotImplemented

            if isinstance(other, SparseArray):
                return _sparse_array_op(self, other, op, op_name)

            elif is_scalar(other):
                with np.errstate(all='ignore'):
                    fill = op(_get_fill(self), np.asarray(other))
                    result = op(self.sp_values, other)

                if op_name == 'divmod':
                    left, right = result
                    lfill, rfill = fill
                    return (_wrap_result(op_name, left, self.sp_index, lfill),
                            _wrap_result(op_name, right, self.sp_index, rfill))

                return _wrap_result(op_name, result, self.sp_index, fill)

            else:
                other = np.asarray(other)
                with np.errstate(all='ignore'):
                    # TODO: delete sparse stuff in core/ops.py
                    # TODO: look into _wrap_result
                    if len(self) != len(other):
                        raise AssertionError(
                            ("length mismatch: {self} vs. {other}".format(
                                self=len(self), other=len(other))))
                    if not isinstance(other, SparseArray):
                        dtype = getattr(other, 'dtype', None)
                        other = SparseArray(other, fill_value=self.fill_value,
                                            dtype=dtype)
                    return _sparse_array_op(self, other, op, op_name)

        name = '__{name}__'.format(name=op.__name__)
        return compat.set_function_name(sparse_arithmetic_method, name, cls)
