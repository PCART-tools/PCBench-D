    def view(self, *args, **kwargs):
        result = super(Index, self).view(*args, **kwargs)
        if isinstance(result, Index):
            result._id = self._id
        return result
