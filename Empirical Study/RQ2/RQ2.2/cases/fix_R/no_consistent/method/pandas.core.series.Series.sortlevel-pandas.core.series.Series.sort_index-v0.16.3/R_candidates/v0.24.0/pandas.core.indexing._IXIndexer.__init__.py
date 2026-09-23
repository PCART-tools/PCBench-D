    def __init__(self, name, obj):
        warnings.warn(self._ix_deprecation_warning,
                      DeprecationWarning, stacklevel=2)
        super(_IXIndexer, self).__init__(name, obj)
