@with_native_function
def cpp_arguments(f: NativeFunction) -> Sequence[Binding]:
    return CppSignatureGroup.from_native_function(f, method=False).signature.arguments()
