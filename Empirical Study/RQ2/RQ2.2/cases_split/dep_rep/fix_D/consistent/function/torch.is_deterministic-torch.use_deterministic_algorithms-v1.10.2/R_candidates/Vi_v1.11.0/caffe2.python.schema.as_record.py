def as_record(value):
    if isinstance(value, Field):
        return value
    elif isinstance(value, list) or isinstance(value, tuple):
        is_field_list = all(
            f is tuple and len(f) == 2 and isinstance(f[0], basestring)
            for f in value
        )
        if is_field_list:
            return Struct(* [(k, as_record(v)) for k, v in value])
        else:
            return Tuple(* [as_record(f) for f in value])
    elif isinstance(value, dict):
        return Struct(* [(k, as_record(v)) for k, v in viewitems(value)])
    else:
        return _normalize_field(value)
