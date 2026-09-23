    def _validate_index_level(self, level):
        """
        Validate index level.

        For single-level Index getting level number is a no-op, but some
        verification must be done like in MultiIndex.

        """
        if isinstance(level, int):
            if level < 0 and level != -1:
                raise IndexError("Too many levels: Index has only 1 level,"
                                 " %d is not a valid level number" % (level, ))
            elif level > 0:
                raise IndexError("Too many levels:"
                                 " Index has only 1 level, not %d" %
                                 (level + 1))
        elif level != self.name:
            raise KeyError('Level %s must be same as name (%s)' %
                           (level, self.name))
