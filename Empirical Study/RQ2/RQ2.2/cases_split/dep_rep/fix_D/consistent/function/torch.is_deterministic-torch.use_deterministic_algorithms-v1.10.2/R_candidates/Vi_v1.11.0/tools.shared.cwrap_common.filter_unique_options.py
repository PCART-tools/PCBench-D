def filter_unique_options(
    options: Iterable[Option],
    allow_kwarg: bool,
    type_to_signature: Dict[str, str],
    remove_self: bool,
) -> List[Option]:
    def exclude_arg(arg: Arg) -> bool:
        return arg['type'] == 'CONSTANT'  # type: ignore[no-any-return]

    def exclude_arg_with_self_check(arg: Arg) -> bool:
        return exclude_arg(arg) or (remove_self and arg['name'] == 'self')

    def signature(option: Option, num_kwarg_only: int) -> str:
        if num_kwarg_only == 0:
            kwarg_only_count = None
        else:
            kwarg_only_count = -num_kwarg_only
        arg_signature = '#'.join(
            type_to_signature.get(arg['type'], arg['type'])
            for arg in option['arguments'][:kwarg_only_count]
            if not exclude_arg_with_self_check(arg))
        if kwarg_only_count is None:
            return arg_signature
        kwarg_only_signature = '#'.join(
            arg['name'] + '#' + arg['type']
            for arg in option['arguments'][kwarg_only_count:]
            if not exclude_arg(arg))
        return arg_signature + "#-#" + kwarg_only_signature
    seen_signatures = set()
    unique = []
    for option in options:
        # if only check num_kwarg_only == 0 if allow_kwarg == False
        limit = len(option['arguments']) if allow_kwarg else 0
        for num_kwarg_only in range(0, limit + 1):
            sig = signature(option, num_kwarg_only)
            if sig not in seen_signatures:
                if num_kwarg_only > 0:
                    for arg in option['arguments'][-num_kwarg_only:]:
                        arg['kwarg_only'] = True
                unique.append(option)
                seen_signatures.add(sig)
                break
    return unique
