@with_native_function
def gen_namedtuple_typename_key(f: NativeFunction) -> str:
    name = cpp.name(f.func)
    fieldnames = namedtuple_fieldnames(f.func.returns)
    return '_'.join([name] + fieldnames)
