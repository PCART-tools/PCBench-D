    def _get_level_number(self, level):
        if not isinstance(level, int):
            if level != self.name:
                raise AssertionError('Level %s must be same as name (%s)'
                                     % (level, self.name))
            level = 0
        return level
