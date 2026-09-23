    def _validate_slicer(self, key, f):
        """ validate and raise if needed on a slice indexers according to the
        passed in function """

        if not f(key.start):
            self._convert_indexer_error(key.start, 'slice start value')
        if not f(key.stop):
            self._convert_indexer_error(key.stop, 'slice stop value')
        if not f(key.step):
            self._convert_indexer_error(key.step, 'slice step value')
