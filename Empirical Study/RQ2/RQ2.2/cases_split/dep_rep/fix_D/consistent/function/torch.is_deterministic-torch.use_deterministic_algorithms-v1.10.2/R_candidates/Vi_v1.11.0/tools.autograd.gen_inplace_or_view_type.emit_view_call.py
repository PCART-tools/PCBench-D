def emit_view_call(f: NativeFunction, input_base: str, unpacked_args: Sequence[str]) -> str:
    # View replay functions use the standard Dispatcher::call API.
    return CALL_DISPATCH.substitute(
        unambiguous_name=f.func.name.unambiguous_name(),
        unpacked_args=unpacked_args)
