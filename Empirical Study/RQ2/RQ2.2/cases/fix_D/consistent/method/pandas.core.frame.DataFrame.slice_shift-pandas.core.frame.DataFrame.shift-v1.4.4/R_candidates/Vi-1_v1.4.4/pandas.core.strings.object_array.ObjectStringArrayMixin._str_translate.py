    def _str_translate(self, table):
        return self._str_map(lambda x: x.translate(table))
