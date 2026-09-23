    def _validate_slicer(self, key, f):
        """ validate and raise if needed on a slice indexers according to the
        passed in function """

        for c in ['start','stop','step']:
            if not f(getattr(key,c)):
                self._convert_indexer_error(key.start, 'slice {0} value'.format(c))
