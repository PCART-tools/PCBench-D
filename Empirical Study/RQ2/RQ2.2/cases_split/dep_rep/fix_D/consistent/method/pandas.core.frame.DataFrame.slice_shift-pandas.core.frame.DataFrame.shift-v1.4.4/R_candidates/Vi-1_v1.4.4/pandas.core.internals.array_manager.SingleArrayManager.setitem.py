    def setitem(self, indexer, value):
        """
        Set values with indexer.

        For SingleArrayManager, this backs s[indexer] = value

        See `setitem_inplace` for a version that works inplace and doesn't
        return a new Manager.
        """
        return self.apply_with_block("setitem", indexer=indexer, value=value)
