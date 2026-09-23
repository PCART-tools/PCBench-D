def instantiate_user_defined_class_object(cls, /, *args, **kwargs):
    obj = cls.__new__(cls, *args, **kwargs)

    # Only call __init__ if the object is an instance of the class
    # Reference: https://github.com/python/cpython/blob/3.12/Objects/typeobject.c#L1670-L1673
    if isinstance(obj, cls):
        obj.__init__(*args, **kwargs)
    return obj
