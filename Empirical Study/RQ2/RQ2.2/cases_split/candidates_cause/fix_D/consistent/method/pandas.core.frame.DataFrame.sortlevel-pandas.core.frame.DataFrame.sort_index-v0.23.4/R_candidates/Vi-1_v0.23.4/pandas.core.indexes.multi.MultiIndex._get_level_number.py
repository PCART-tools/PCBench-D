    def _get_level_number(self, level):
        try:
            count = self.names.count(level)
            if count > 1:
                raise ValueError('The name %s occurs multiple times, use a '
                                 'level number' % level)
            level = self.names.index(level)
        except ValueError:
            if not isinstance(level, int):
                raise KeyError('Level %s not found' % str(level))
            elif level < 0:
                level += self.nlevels
                if level < 0:
                    orig_level = level - self.nlevels
                    raise IndexError('Too many levels: Index has only %d '
                                     'levels, %d is not a valid level number' %
                                     (self.nlevels, orig_level))
            # Note: levels are zero-based
            elif level >= self.nlevels:
                raise IndexError('Too many levels: Index has only %d levels, '
                                 'not %d' % (self.nlevels, level + 1))
        return level
