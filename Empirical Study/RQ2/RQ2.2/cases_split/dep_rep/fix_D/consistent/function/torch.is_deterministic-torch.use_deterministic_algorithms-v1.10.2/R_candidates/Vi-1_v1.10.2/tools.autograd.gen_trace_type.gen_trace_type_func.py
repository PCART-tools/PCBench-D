def gen_trace_type_func(
    fn: NativeFunction
) -> Dict[str, List[str]]:
    return {
        'trace_method_definitions': [method_definition(fn)],
        'trace_wrapper_registrations': [method_registration(fn)],
    }
