    def _get_index(self, name):
        """ safe get index, translate keys for datelike to underlying repr """
        return self._get_indices([name])[0]
