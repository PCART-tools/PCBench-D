def group_filter_overloads(
    pairs: Sequence[PythonSignatureNativeFunctionPair],
    pred: Callable[[NativeFunction], bool]
) -> Dict[BaseOperatorName, List[PythonSignatureNativeFunctionPair]]:
    grouped: Dict[BaseOperatorName, List[PythonSignatureNativeFunctionPair]] = defaultdict(list)
    for pair in pairs:
        if pred(pair.function):
            grouped[pair.function.func.name.name].append(pair)
    return grouped
