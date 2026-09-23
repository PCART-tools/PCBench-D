    def _convert_indexer_error(self, key, msg=None):
        if msg is None:
            msg = 'label'
        raise TypeError("the {0} [{1}] is not a proper indexer for this index "
                        "type ({2})".format(msg, key, self.__class__.__name__))
