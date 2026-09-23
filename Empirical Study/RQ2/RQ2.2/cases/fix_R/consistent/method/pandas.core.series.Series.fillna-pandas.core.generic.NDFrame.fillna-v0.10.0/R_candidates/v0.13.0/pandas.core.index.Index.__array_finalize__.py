    def __array_finalize__(self, obj):
        self._reset_identity()
        if not isinstance(obj, type(self)):
            # Only relevant if array being created from an Index instance
            return

        self.name = getattr(obj, 'name', None)
