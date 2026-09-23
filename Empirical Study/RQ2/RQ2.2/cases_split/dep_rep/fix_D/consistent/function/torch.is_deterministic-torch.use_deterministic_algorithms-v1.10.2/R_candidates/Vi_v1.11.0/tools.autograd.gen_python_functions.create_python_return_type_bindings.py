def create_python_return_type_bindings(
    fm: FileManager,
    pairs: Sequence[PythonSignatureNativeFunctionPair],
    pred: Callable[[NativeFunction], bool],
    filename: str,
) -> None:
    """
    Generate function to initialize and return named tuple for native functions
    which returns named tuple and relevant entry for the map in `python_return_types.cpp`.
    """
    py_return_types_definition: List[str] = []
    py_return_types_map: List[str] = []

    grouped = group_filter_overloads(pairs, pred)

    for name in sorted(grouped.keys(), key=lambda x: str(x)):
        overloads = grouped[name]
        definitions, map_entries = generate_return_type_definition_and_map_entry(overloads)
        py_return_types_definition.append("" if not definitions else "\n".join(definitions))
        py_return_types_map.append("" if not map_entries else "\n".join(map_entries))

    fm.write_with_template(filename, filename, lambda: {
        'generated_comment': '@' + f'generated from {fm.template_dir}/{filename}',
        'py_return_types': py_return_types_definition,
        'py_return_types_map' : py_return_types_map,
    })
