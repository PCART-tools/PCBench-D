    def _wrap_applied_output(
        self,
        data,
        values: list,
        not_indexed_same: bool = False,
        is_transform: bool = False,
    ):
        raise AbstractMethodError(self)
