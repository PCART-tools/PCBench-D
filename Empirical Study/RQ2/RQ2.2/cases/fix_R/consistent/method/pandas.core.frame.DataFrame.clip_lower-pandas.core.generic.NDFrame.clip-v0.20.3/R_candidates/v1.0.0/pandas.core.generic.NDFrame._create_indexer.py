    @classmethod
    def _create_indexer(cls, name: str, indexer) -> None:
        """Create an indexer like _name in the class.

        Kept for compatibility with geopandas. To be removed in the future. See GH27258
        """
        if getattr(cls, name, None) is None:
            _indexer = functools.partial(indexer, name)
            setattr(cls, name, property(_indexer, doc=indexer.__doc__))
