    def _wrap_applied_output(
        self,
        data,
        values: list,
        not_indexed_same: bool = False,
        override_group_keys: bool = False,
    ):
        raise AbstractMethodError(self)
