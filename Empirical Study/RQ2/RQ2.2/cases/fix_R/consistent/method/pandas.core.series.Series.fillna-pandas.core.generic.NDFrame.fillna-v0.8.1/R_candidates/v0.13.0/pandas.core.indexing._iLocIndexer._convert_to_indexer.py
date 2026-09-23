    def _convert_to_indexer(self, obj, axis=0, is_setter=False):
        """ much simpler as we only have to deal with our valid types """
        if self._has_valid_type(obj, axis):
            return obj

        raise ValueError("Can only index by location with a [%s]" %
                         self._valid_types)
