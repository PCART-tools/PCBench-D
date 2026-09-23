    @classmethod
    def _import_from_c(cls, name: str, pointers: list[tuple[int, int]]) -> Self:
        """
        Construct a Series from Arrows C interface.

        Warning
        -------
        This will read the `array` pointer without moving it. The host process should
        garbage collect the heap pointer, but not its contents.
        """
        return cls._from_pyseries(PySeries._import_from_c(name, pointers))
