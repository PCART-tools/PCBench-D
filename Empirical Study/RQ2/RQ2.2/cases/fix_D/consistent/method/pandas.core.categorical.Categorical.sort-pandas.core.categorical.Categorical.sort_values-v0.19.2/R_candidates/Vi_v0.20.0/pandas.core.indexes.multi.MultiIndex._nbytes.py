    def _nbytes(self, deep=False):
        """
        return the number of bytes in the underlying data
        deeply introspect the level data if deep=True

        include the engine hashtable

        *this is in internal routine*

        """
        level_nbytes = sum((i.memory_usage(deep=deep) for i in self.levels))
        label_nbytes = sum((i.nbytes for i in self.labels))
        names_nbytes = sum((getsizeof(i) for i in self.names))
        result = level_nbytes + label_nbytes + names_nbytes

        # include our engine hashtable
        result += self._engine.sizeof(deep=deep)
        return result
