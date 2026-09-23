def emit_view_call(f: NativeFunction, input_base: str, unpacked_args: Sequence[str]) -> str:
    # View replay functions use the standard Dispatcher::call API.
    if Variant.function in f.variants:
        call = CALL_DISPATCH_VIA_NAMESPACE.substitute(
            api_name=cpp.name(
                f.func,
                faithful_name_for_out_overloads=True,
            ),
            unpacked_args=unpacked_args)
    else:
        call = CALL_DISPATCH_VIA_METHOD.substitute(
            api_name=cpp.name(f.func),
            var=input_base,
            unpacked_method_args=unpacked_args[1:])
    return call
