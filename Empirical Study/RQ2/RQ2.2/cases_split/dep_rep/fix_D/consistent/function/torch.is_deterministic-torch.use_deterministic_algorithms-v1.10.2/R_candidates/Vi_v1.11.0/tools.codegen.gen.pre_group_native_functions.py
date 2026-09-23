def pre_group_native_functions(
        native_functions: Sequence[NativeFunction]) -> Dict[FunctionSchema, Dict[SchemaKind, NativeFunction]]:
    pre_grouped_native_functions: Dict[FunctionSchema, Dict[SchemaKind, NativeFunction]] = defaultdict(dict)
    for f in native_functions:
        d = pre_grouped_native_functions[f.func.signature()]
        assert f.func.kind() not in d
        d[f.func.kind()] = f
    return pre_grouped_native_functions
