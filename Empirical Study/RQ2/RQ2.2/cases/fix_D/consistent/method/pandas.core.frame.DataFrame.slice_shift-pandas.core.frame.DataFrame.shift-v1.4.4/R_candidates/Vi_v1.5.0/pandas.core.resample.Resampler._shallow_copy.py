    @final
    def _shallow_copy(self, obj, **kwargs):
        """
        return a new object with the replacement attributes
        """
        if isinstance(obj, self._constructor):
            obj = obj.obj
        for attr in self._attributes:
            if attr not in kwargs:
                kwargs[attr] = getattr(self, attr)
        return self._constructor(obj, **kwargs)
