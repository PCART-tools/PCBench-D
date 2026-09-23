    def to_native_types(self, slicer=None, **kwargs):
        """ slice and dice then format """
        values = self
        if slicer is not None:
            values = values[slicer]
        return values._format_native_types(**kwargs)
