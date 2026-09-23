    @classmethod
    def _from_arrow(cls, name: str, values: pa.Array, *, rechunk: bool = True) -> Self:
        """Construct a Series from an Arrow Array."""
        return cls._from_pyseries(arrow_to_pyseries(name, values, rechunk=rechunk))
