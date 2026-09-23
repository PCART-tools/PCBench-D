def NamedTuple(name_prefix, *fields):
    return Struct(* [('%s_%d' % (name_prefix, i), field)
                     for i, field in enumerate(fields)])
