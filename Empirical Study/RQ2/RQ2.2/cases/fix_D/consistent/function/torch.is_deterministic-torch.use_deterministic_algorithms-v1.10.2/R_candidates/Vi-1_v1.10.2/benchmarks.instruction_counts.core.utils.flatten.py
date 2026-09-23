def flatten(schema: Definition) -> FlatIntermediateDefinition:
    """See types.py for an explanation of nested vs. flat definitions."""
    result: FlatIntermediateDefinition = {}
    _flatten(key_prefix=(), sub_schema=schema, result=result)

    # Ensure that we produced a valid flat definition.
    for k, v in result.items():
        assert isinstance(k, tuple)
        assert all(isinstance(ki, str) for ki in k)
        assert isinstance(v, (TimerArgs, GroupedBenchmark))
    return result
