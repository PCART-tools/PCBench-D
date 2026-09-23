    def _cmp_method(self, other, op):
        res_name = ops.get_op_result_name(self, other)

        if isinstance(other, Series) and not self._indexed_same(other):
            raise ValueError("Can only compare identically-labeled Series objects")

        lvalues = self._values
        rvalues = extract_array(other, extract_numpy=True, extract_range=True)

        with np.errstate(all="ignore"):
            res_values = ops.comparison_op(lvalues, rvalues, op)

        return self._construct_result(res_values, name=res_name)
