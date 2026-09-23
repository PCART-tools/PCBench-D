@with_native_function
def method_registration(f: NativeFunction) -> str:
    assert cpp.name(f.func) not in MANUAL_TRACER

    return WRAPPER_REGISTRATION.substitute(
        name=f.func.name,
        type_wrapper_name=type_wrapper_name(f),
        class_type='TraceType',
    )
