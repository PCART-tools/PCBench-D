    def __contains__(self, key: Union[int, np.integer]) -> bool:
        hash(key)
        try:
            key = ensure_python_int(key)
        except TypeError:
            return False
        return key in self._range
