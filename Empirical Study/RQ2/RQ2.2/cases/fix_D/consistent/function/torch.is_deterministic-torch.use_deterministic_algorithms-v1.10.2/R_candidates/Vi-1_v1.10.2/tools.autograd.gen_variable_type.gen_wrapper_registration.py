@with_native_function
def gen_wrapper_registration(f: NativeFunction) -> str:
    return WRAPPER_REGISTRATION.substitute(
        unqual_operator_name_with_overload=f.func.name,
        type_wrapper_name=type_wrapper_name(f),
        class_type='VariableType',
    )
