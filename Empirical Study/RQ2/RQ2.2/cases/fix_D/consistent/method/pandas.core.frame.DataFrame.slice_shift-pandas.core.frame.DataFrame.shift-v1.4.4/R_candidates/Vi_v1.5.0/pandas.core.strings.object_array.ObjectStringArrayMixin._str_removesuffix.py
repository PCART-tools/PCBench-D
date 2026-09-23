    def _str_removesuffix(self, suffix: str) -> Series:
        # this could be used on Python 3.9+
        # f = lambda x: x.removesuffix(suffix)
        # return self._str_map(str.removesuffix)

        def removesuffix(text: str) -> str:
            if text.endswith(suffix):
                return text[: -len(suffix)]
            return text

        return self._str_map(removesuffix)
