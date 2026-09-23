def _exec(obj):
    # exec on PyQt6, exec_ elsewhere.
    obj.exec() if hasattr(obj, "exec") else obj.exec_()
