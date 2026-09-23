def declare_returned_variables(f: NativeFunction) -> str:
    modifies_arguments = f.func.kind() in (SchemaKind.inplace, SchemaKind.out)
    if modifies_arguments:
        return ''
    if len(f.func.returns) == 1:
        return ''
    types = map(cpp.return_type, f.func.returns)
    names = cpp.return_names(f)
    return '\n'.join(f'{type.cpp_type()} {name};' for type, name in zip(types, names))
