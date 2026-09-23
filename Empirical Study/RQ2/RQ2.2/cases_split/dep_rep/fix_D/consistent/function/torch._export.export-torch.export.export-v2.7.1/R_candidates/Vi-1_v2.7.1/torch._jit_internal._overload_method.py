def _overload_method(func):
    _check_overload_body(func)
    qual_name = _qualified_name(func)
    global _overloaded_methods
    class_name_map = _overloaded_methods.get(qual_name, None)
    if class_name_map is None:
        class_name_map = {}
        _overloaded_methods[qual_name] = class_name_map

    class_name, line_no = get_class_name_lineno(func)
    method_overloads = class_name_map.get(class_name, None)
    if method_overloads is None:
        method_overloads = []
        class_name_map[class_name] = method_overloads
        _overloaded_method_class_fileno[(qual_name, class_name)] = line_no
    else:
        existing_lineno = _overloaded_method_class_fileno[(qual_name, class_name)]
        if existing_lineno != line_no:
            raise RuntimeError(
                "Cannot currently overload the same method name in two different"
                " classes with the same name in the same module"
            )

    method_overloads.append(func)
    return func
