def arguments(func: FunctionSchema) -> List[Binding]:
    return [argument(a) for a in jit_arguments(func)]
