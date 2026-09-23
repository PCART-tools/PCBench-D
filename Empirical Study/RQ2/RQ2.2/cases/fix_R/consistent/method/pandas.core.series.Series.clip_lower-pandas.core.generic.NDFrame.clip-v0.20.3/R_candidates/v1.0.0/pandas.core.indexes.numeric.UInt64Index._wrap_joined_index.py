    def _wrap_joined_index(self, joined, other):
        name = get_op_result_name(self, other)
        return UInt64Index(joined, name=name)
