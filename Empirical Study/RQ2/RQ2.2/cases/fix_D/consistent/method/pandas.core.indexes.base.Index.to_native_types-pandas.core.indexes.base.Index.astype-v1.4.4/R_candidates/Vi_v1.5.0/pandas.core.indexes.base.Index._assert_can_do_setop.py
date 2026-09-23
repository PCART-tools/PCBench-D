    @final
    def _assert_can_do_setop(self, other) -> bool:
        if not is_list_like(other):
            raise TypeError("Input must be Index or array-like")
        return True
