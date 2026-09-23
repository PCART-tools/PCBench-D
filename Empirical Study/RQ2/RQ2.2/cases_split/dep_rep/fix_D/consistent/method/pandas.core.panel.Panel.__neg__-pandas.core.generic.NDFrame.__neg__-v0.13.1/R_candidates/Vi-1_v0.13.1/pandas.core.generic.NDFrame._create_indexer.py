    @classmethod
    def _create_indexer(cls, name, indexer):
        """ create an indexer like _name in the class """

        if getattr(cls, name, None) is None:
            iname = '_%s' % name
            setattr(cls, iname, None)

            def _indexer(self):
                i = getattr(self, iname)
                if i is None:
                    i = indexer(self, name)
                    setattr(self, iname, i)
                return i

            setattr(cls, name, property(_indexer))

            # add to our internal names set
            cls._internal_names_set.add(iname)
