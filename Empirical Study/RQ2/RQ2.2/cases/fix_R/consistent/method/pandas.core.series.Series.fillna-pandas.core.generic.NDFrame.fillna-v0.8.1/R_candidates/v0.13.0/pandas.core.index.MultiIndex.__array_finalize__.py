    def __array_finalize__(self, obj):
        """
        Update custom MultiIndex attributes when a new array is created by
        numpy, e.g. when calling ndarray.view()
        """
        # overriden if a view
        self._reset_identity()
        if not isinstance(obj, type(self)):
            # Only relevant if this array is being created from an Index
            # instance.
            return

        # skip the validation on first, rest will catch the errors
        self._set_levels(getattr(obj, 'levels', []), validate=False)
        self._set_labels(getattr(obj, 'labels', []))
        self._set_names(getattr(obj, 'names', []))
        self.sortorder = getattr(obj, 'sortorder', None)
