    def _set_names(self, values, level=None):
        if len(values) != 1:
            raise ValueError('Length of new names must be 1, got %d' %
                             len(values))
        self.name = values[0]
