    def _can_be_inplace(_other):
        return not (
            isinstance(_other.data, ir.BaseView)
            or len(_other.get_inputs_that_alias_output()) > 0
        )
