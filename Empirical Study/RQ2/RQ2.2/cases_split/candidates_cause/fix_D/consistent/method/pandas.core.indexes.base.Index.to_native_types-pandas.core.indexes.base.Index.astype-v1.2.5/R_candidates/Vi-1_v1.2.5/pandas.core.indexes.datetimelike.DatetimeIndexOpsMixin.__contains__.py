    @Appender(Index.__contains__.__doc__)
    def __contains__(self, key: Any) -> bool:
        hash(key)
        try:
            res = self.get_loc(key)
        except (KeyError, TypeError, ValueError):
            return False
        return bool(
            is_scalar(res) or isinstance(res, slice) or (is_list_like(res) and len(res))
        )
