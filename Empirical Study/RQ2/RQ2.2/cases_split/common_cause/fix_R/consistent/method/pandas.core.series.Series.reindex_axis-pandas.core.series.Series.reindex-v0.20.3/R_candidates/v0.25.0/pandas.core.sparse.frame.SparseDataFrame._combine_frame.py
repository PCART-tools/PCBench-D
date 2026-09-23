    def _combine_frame(self, other, func, fill_value=None, level=None):
        if level is not None:
            raise NotImplementedError("'level' argument is not supported")

        this, other = self.align(other, join="outer", level=level, copy=False)
        new_index, new_columns = this.index, this.columns

        if self.empty and other.empty:
            return self._constructor(index=new_index).__finalize__(self)

        new_data = {}
        if fill_value is not None:
            # TODO: be a bit more intelligent here
            for col in new_columns:
                if col in this and col in other:
                    dleft = this[col].to_dense()
                    dright = other[col].to_dense()
                    result = dleft._binop(dright, func, fill_value=fill_value)
                    result = result.to_sparse(fill_value=this[col].fill_value)
                    new_data[col] = result
        else:

            for col in new_columns:
                if col in this and col in other:
                    new_data[col] = func(this[col], other[col])

        new_fill_value = self._get_op_result_fill_value(other, func)

        return self._constructor(
            data=new_data,
            index=new_index,
            columns=new_columns,
            default_fill_value=new_fill_value,
        ).__finalize__(self)
