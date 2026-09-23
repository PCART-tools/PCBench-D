def dispatch_lambda_args(ps: PythonSignature, f: NativeFunction) -> Tuple[DispatchLambdaArgument, ...]:
    # Start with cpp arguments - dispatch lambda signature always include 'self'
    cpp_args: Sequence[Binding] = _cpp_signature(f, method=False).arguments()

    # Special reorder logic for deprecated python signature
    if isinstance(ps, PythonSignatureDeprecated):
        m: Dict[str, Binding] = dict((a.name, a) for a in cpp_args)
        # reorder according to the deprecated signature
        # ignore 'out' argument when binding to non-output function.
        ordered_args = filter(lambda n: n != 'out' or f.func.is_out_fn(),
                              ps.deprecated_args_names)
        cpp_args = list(map(lambda n: m[n], ordered_args))

    out_args: Set[str] = set(a.name for a in f.func.arguments.out)

    # Convert from cpp argument to lambda argument
    def dispatch_lambda_arg(cpp_arg: Binding) -> DispatchLambdaArgument:
        type_str = cpp_arg.type
        is_out_arg = cpp_arg.name in out_args
        if ps.method and cpp_arg.name == 'self':
            # For method's 'self', we can use 'const Tensor &' and simply ignore mutability!
            type_str = 'const at::Tensor &'
        else:
            # For other cases we need prevent dangling refs to temps (unless it's
            # unpacked scattered output)
            # The reason is explained in the comments above and in 'dispatch_lambda_return_str()'.
            # TODO: avoid this special handling?
            ensure_temp_safe = len(out_args) <= 1 or not is_out_arg
            if ensure_temp_safe:
                type_str = {
                    'at::Tensor &': 'at::Tensor',
                }.get(type_str, type_str)
        return DispatchLambdaArgument(
            name=cpp_arg.name,
            type_str=type_str,
            is_out_arg=is_out_arg,
        )

    return tuple(map(dispatch_lambda_arg, cpp_args))
