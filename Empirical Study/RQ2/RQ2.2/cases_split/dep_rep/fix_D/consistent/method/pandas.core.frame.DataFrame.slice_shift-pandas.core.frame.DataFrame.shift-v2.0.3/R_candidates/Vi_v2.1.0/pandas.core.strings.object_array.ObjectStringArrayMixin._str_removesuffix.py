    def _str_removesuffix(self, suffix: str) -> Series:
        return self._str_map(lambda x: x.removesuffix(suffix))
