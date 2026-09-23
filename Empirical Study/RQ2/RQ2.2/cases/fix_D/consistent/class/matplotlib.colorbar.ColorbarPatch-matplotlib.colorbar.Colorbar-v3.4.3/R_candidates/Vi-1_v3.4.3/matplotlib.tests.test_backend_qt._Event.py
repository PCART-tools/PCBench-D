    class _Event:
        def isAutoRepeat(self): return False
        def key(self): return getattr(qt_core.Qt, qt_key)
        def modifiers(self): return qt_mod
