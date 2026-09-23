def error_check_native_functions(funcs: Sequence[NativeFunction]) -> None:
    func_map: Dict[OperatorName, NativeFunction] = {}
    base_func_map: Dict[BaseOperatorName, List[NativeFunction]] = defaultdict(list)
    for f in funcs:
        func_map[f.func.name] = f
        base_func_map[f.func.name.name].append(f)
    for f in funcs:
        if f.structured_delegate is not None:
            delegate_func = func_map[f.structured_delegate]
            assert delegate_func.structured, \
                f"{f.func.name} is marked as a structured_delegate pointing to " \
                f"{f.structured_delegate}, but {f.structured_delegate} is not marked as structured. " \
                f"Consider adding 'structured=True' to the delegated operator"
        if f.tag is not None and f.tag is Tag.inplace_view:
            base_name = f.func.name.name
            overload_name = f.func.name.overload_name
            assert base_name.inplace, \
                f"{f.func.name} is marked with tag: inplace_view, but it doesn't follow the naming " \
                "convention for inplace ops - the codegen expects the base name to have a trailing underscore. "
            out_of_place_base_name = BaseOperatorName(base_name.base, False, base_name.dunder_method)
            assert len(base_func_map[out_of_place_base_name]) > 0, \
                f"{f.func.name} is marked with tag: inplace_view. The codegen expects there to be a corresponding " \
                f"out-of-place view op with the name '{base_name}' and matching schema, but it didn't find one. "
