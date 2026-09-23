    def __init__(self, name, obj):
        warnings.warn(self._ix_deprecation_warning, FutureWarning, stacklevel=2)
        super().__init__(name, obj)
