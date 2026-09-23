    @property
    def return_type(self):
        # clobber types to bool if the op is a boolean operator
        if self.op in (CMP_OPS_SYMS + BOOL_OPS_SYMS):
            return np.bool_
        return result_type_many(*(term.type for term in com.flatten(self)))
