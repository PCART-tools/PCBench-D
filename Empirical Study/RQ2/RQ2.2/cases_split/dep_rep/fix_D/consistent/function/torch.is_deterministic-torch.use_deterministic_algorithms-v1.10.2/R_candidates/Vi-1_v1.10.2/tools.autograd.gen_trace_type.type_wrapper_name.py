def type_wrapper_name(f: NativeFunction) -> str:
    if f.func.name.overload_name:
        return f'{cpp.name(f.func)}_{f.func.name.overload_name}'
    else:
        return cpp.name(f.func)
