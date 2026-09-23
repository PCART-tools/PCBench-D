    def _invalid_indexer(self, form, key):
        """ consistent invalid indexer message """
        raise TypeError("cannot do {form} indexing on {klass} with these "
                        "indexers [{key}] of {kind}".format(
                            form=form, klass=type(self), key=key,
                            kind=type(key)))
