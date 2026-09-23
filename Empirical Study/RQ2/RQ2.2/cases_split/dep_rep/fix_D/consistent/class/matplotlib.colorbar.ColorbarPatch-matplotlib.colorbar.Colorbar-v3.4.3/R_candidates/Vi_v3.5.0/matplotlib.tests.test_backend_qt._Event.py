    class _Event:
        def isAutoRepeat(self): return False
        def key(self): return _to_int(getattr(_enum("QtCore.Qt.Key"), qt_key))
        def modifiers(self): return qt_mod
