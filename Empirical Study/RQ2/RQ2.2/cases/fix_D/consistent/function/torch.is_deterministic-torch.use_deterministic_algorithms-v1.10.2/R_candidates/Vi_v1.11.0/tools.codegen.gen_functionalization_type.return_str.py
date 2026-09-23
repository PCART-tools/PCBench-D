def return_str(f: NativeFunction) -> str:
    if len(f.func.arguments.out) != 0:
        if len(f.func.arguments.out) > 1:
            return_names = ', '.join(a.name for a in f.func.arguments.out)
            return f'return {DispatcherSignature.from_schema(f.func).returns_type().cpp_type()}({return_names});'
        else:
            return f'return {f.func.arguments.out[0].name}'
    if f.func.arguments.self_arg is not None:
        return f'return {f.func.arguments.self_arg.argument.name}'
    return ''
