def _flatten(
    key_prefix: Label,
    sub_schema: Definition,
    result: FlatIntermediateDefinition
) -> None:
    for k, value in sub_schema.items():
        if isinstance(k, tuple):
            assert all(isinstance(ki, str) for ki in k)
            key_suffix: Label = k
        elif k is None:
            key_suffix = ()
        else:
            assert isinstance(k, str)
            key_suffix = (k,)

        key: Label = key_prefix + key_suffix
        if isinstance(value, (TimerArgs, GroupedBenchmark)):
            assert key not in result, f"duplicate key: {key}"
            result[key] = value
        else:
            assert isinstance(value, dict)
            _flatten(key_prefix=key, sub_schema=value, result=result)
