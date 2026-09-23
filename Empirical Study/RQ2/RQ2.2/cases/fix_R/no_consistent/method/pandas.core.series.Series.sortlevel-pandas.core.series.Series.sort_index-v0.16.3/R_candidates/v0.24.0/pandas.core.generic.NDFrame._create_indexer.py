    @classmethod
    def _create_indexer(cls, name, indexer):
        """Create an indexer like _name in the class."""
        if getattr(cls, name, None) is None:
            _indexer = functools.partial(indexer, name)
            setattr(cls, name, property(_indexer, doc=indexer.__doc__))
