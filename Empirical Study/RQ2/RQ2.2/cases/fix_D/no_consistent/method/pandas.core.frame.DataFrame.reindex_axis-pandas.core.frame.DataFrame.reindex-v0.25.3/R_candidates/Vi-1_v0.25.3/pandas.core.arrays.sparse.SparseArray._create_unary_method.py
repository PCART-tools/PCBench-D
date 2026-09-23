    @classmethod
    def _create_unary_method(cls, op):
        def sparse_unary_method(self):
            fill_value = op(np.array(self.fill_value)).item()
            values = op(self.sp_values)
            dtype = SparseDtype(values.dtype, fill_value)
            return cls._simple_new(values, self.sp_index, dtype)

        name = "__{name}__".format(name=op.__name__)
        return compat.set_function_name(sparse_unary_method, name, cls)
