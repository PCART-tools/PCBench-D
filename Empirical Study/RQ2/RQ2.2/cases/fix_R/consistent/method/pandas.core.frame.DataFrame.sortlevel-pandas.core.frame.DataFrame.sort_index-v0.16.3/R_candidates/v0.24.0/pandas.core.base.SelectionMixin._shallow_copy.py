    def _shallow_copy(self, obj=None, obj_type=None, **kwargs):
        """
        return a new object with the replacement attributes
        """
        if obj is None:
            obj = self._selected_obj.copy()
        if obj_type is None:
            obj_type = self._constructor
        if isinstance(obj, obj_type):
            obj = obj.obj
        for attr in self._attributes:
            if attr not in kwargs:
                kwargs[attr] = getattr(self, attr)
        return obj_type(obj, **kwargs)
