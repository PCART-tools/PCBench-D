def arguments(func: FunctionSchema) -> List[Binding]:
    args: List[Union[Argument, TensorOptionsArguments, SelfArgument]] = []
    args.extend(func.arguments.non_out)
    args.extend(func.arguments.out)
    return [r for arg in args for r in argument(arg, is_out=func.is_out_fn())]
