def arguments(
    arguments: Arguments,
    *, faithful: bool, method: bool, cpp_no_default_args: Set[str]
) -> List[Binding]:
    args: List[Union[Argument, TensorOptionsArguments, SelfArgument]] = []
    if faithful:
        args.extend(arguments.non_out)
        args.extend(arguments.out)
    else:
        args.extend(arguments.out)
        args.extend(arguments.non_out)
    return [
        r.no_default() if faithful else r for a in args
        for r in argument(
            a, faithful=faithful, method=method,
            has_tensor_options=arguments.tensor_options is not None,
            cpp_no_default_args=cpp_no_default_args)
    ]
