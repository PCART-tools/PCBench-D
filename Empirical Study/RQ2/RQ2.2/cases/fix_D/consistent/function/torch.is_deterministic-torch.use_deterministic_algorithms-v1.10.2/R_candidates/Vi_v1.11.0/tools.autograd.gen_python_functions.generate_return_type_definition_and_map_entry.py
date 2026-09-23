def generate_return_type_definition_and_map_entry(
    overloads: Sequence[PythonSignatureNativeFunctionPair],
) -> Tuple[List[str], List[str]]:
    """
    Generate block of function in `python_return_types.cpp` to initialize
    and return named tuple for a native function which returns named tuple
    and relevant entry for the map in same file.
    """
    typenames: Dict[str, str] = {}  # map from unique name + field name lists to typedef name
    definitions: List[str] = []  # function defintion to register the typedef
    map_entries: List[str] = []  # C++ map entry of <function_name, function creates it namedtuple>

    for overload in overloads:
        fieldnames = namedtuple_fieldnames(overload.function.func.returns)
        if not fieldnames:
            continue

        fields = ', '.join(f'{{"{fn}", ""}}' for fn in fieldnames)

        name = cpp.name(overload.function.func)  # use @with_native_function?
        tn_key = gen_namedtuple_typename_key(overload.function)
        typename = typenames.get(tn_key)

        if typename is None:
            typename = f'{name}NamedTuple{"" if not definitions else len(definitions)}'
            typenames[tn_key] = typename
            definitions.append(f"""\
PyTypeObject* get_{name}_namedtuple() {{
    static PyStructSequence_Field NamedTuple_fields[] = {{ {fields},  {{nullptr}} }};
    static PyTypeObject {typename};
    static bool is_initialized = false;
    static PyStructSequence_Desc desc = {{ "torch.return_types.{name}", nullptr, NamedTuple_fields, {len(fieldnames)} }};
    if (!is_initialized) {{
        PyStructSequence_InitType(&{typename}, &desc);
        {typename}.tp_repr = (reprfunc)torch::utils::returned_structseq_repr;
        is_initialized = true;
    }}
    return &{typename};
}}
""")
            map_entries.append(f'{{"{name}", get_{name}_namedtuple()}}, ')

    return definitions, map_entries
