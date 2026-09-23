def EnumClassKeyVals(cls):
    # cls can only be derived from object
    assert type(cls) == type
    # Enum attribute keys are all capitalized and values are strings
    enum = {}
    for k in dir(cls):
        if k == k.upper():
            v = getattr(cls, k)
            if isinstance(v, string_types):
                assert v not in enum.values(), (
                    "Failed to resolve {} as Enum: "
                    "duplicate entries {}={}, {}={}".format(
                        cls, k, v, [key for key in enum if enum[key] == v][0], v
                    )
                )
                enum[k] = v
    return enum
