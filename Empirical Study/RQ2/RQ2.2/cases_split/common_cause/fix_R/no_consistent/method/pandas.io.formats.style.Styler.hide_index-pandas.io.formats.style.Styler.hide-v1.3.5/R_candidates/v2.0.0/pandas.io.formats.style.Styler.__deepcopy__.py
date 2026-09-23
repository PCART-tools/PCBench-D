    def __deepcopy__(self, memo) -> Styler:
        return self._copy(deepcopy=True)
