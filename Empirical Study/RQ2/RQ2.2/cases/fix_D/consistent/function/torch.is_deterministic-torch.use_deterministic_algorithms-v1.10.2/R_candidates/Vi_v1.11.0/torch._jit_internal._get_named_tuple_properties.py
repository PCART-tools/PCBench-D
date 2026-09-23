def _get_named_tuple_properties(obj):
    assert issubclass(obj, tuple) and hasattr(obj, '_fields')
    if hasattr(obj, "_field_defaults"):
        defaults = [obj._field_defaults[field]
                    for field in obj._fields
                    if field in obj._field_defaults]
    else:
        defaults = []
    annotations = []
    has_annotations = hasattr(obj, '__annotations__')
    for field in obj._fields:
        if has_annotations and field in obj.__annotations__:
            the_type = torch.jit.annotations.ann_to_type(obj.__annotations__[field], fake_range())
            annotations.append(the_type)
        else:
            annotations.append(torch._C.TensorType.getInferred())
    return type(obj).__name__, obj._fields, annotations, defaults
