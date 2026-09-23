def jit_arguments(func: FunctionSchema) -> List[Argument]:
    def to_argument(a: Union[Argument, TensorOptionsArguments, SelfArgument]) -> List[Argument]:
        if isinstance(a, Argument):
            return [a]
        elif isinstance(a, SelfArgument):
            return [a.argument]
        elif isinstance(a, TensorOptionsArguments):
            return [a.dtype, a.layout, a.device, a.pin_memory]
        else:
            assert_never(a)
    return list(concatMap(to_argument, itertools.chain(
        func.arguments.positional,
        func.arguments.kwarg_only,
        func.arguments.out)))
