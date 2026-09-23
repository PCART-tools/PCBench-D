    def _convert_can_do_setop(self, other) -> tuple[Index, Hashable]:
        if not isinstance(other, Index):
            # TODO(2.0): no need to special-case here once _with_infer
            #  deprecation is enforced
            if hasattr(other, "dtype"):
                other = Index(other, name=self.name, dtype=other.dtype)
            else:
                # e.g. list
                other = Index(other, name=self.name)
            result_name = self.name
        else:
            result_name = get_op_result_name(self, other)
        return other, result_name
