def was_instancecheck_override(obj):
    return type(obj).__dict__.get("__instancecheck__", False)
