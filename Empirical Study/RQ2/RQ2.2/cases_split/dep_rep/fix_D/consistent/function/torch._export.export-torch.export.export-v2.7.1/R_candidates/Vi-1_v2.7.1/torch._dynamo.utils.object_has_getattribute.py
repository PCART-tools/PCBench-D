def object_has_getattribute(value: Any):
    return class_has_getattribute(type(value))
