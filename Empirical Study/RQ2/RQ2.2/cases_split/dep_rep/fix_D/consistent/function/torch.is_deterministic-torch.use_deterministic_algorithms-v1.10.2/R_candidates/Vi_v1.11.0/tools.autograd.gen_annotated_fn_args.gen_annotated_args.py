@with_native_function
def gen_annotated_args(f: NativeFunction) -> str:
    out_args: List[Dict[str, Any]] = []
    for arg in f.func.arguments.flat_positional:
        if arg.default is not None:
            continue
        out_arg: Dict[str, Any] = {}
        out_arg['name'] = arg.name
        out_arg['simple_type'] = python.argument_type_str(arg.type, simple_type=True)
        size = python.argument_type_size(arg.type)
        if size:
            out_arg['size'] = size
        out_args.append(out_arg)

    return f'{f.func.name.name}: {repr(out_args)},'
