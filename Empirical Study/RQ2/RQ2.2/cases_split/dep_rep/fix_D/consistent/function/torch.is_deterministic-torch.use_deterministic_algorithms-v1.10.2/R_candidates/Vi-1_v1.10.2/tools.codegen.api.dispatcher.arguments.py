def arguments(func: FunctionSchema) -> List[Binding]:
    return [
        Binding(
            nctype=argument_type(a, binds=a.name),
            name=a.name,
            argument=a,
        ) for a in jit_arguments(func)]
