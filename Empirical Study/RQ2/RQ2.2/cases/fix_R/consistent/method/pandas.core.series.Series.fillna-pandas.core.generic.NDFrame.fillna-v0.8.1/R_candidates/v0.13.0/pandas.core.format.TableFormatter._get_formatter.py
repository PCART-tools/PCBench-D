    def _get_formatter(self, i):
        if isinstance(self.formatters, (list, tuple)):
            if com.is_integer(i):
                return self.formatters[i]
            else:
                return None
        else:
            if com.is_integer(i) and i not in self.columns:
                i = self.columns[i]
            return self.formatters.get(i, None)
