    def view(self, cls=None):

        # we need to see if we are subclassing an
        # index type here
        if cls is not None and not hasattr(cls,'_typ'):
            result = self._data.view(cls)
        else:
            result = self._shallow_copy()
        if isinstance(result, Index):
            result._id = self._id
        return result
