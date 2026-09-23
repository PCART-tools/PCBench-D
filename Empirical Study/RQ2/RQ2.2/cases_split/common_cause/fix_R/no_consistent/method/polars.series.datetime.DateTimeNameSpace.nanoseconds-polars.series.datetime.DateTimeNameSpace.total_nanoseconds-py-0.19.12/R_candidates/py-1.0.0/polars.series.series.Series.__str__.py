    def __str__(self) -> str:
        s_repr: str = self._s.as_str()
        return s_repr.replace("Series", f"{self.__class__.__name__}", 1)
