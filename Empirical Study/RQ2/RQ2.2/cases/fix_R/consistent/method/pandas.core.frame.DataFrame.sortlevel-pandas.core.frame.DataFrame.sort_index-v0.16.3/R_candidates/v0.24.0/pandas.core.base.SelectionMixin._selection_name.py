    @property
    def _selection_name(self):
        """
        return a name for myself; this would ideally be called
        the 'name' property, but we cannot conflict with the
        Series.name property which can be set
        """
        if self._selection is None:
            return None  # 'result'
        else:
            return self._selection
