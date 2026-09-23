def get_current_scope():
    global _threadlocal_scope
    if not hasattr(_threadlocal_scope, "current_scope"):
        _threadlocal_scope.current_scope = {}
    return _threadlocal_scope.current_scope
