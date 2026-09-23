def name(func: FunctionSchema, *, faithful_name_for_out_overloads: bool = False) -> str:
    name = str(func.name.name)
    if func.is_out_fn():
        if faithful_name_for_out_overloads:
            name += '_outf'
        else:
            name += '_out'

    return name
