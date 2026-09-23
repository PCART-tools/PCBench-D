def parse_full_codegen_ops(
        backend_yaml_path: str,
        grouped_native_functions: Sequence[Union[NativeFunction, NativeFunctionsGroup]],
) -> List[OperatorName]:

    native_functions_map: Dict[OperatorName, NativeFunction] = {
        f.func.name: f
        for f in concatMap(lambda f: [f] if isinstance(f, NativeFunction) else list(f.functions()), grouped_native_functions)
    }

    with open(backend_yaml_path, 'r') as f:
        yaml_values = yaml.load(f, Loader=YamlLoader)
    assert isinstance(yaml_values, dict)

    full_codegen = yaml_values.pop('full_codegen', [])
    assert isinstance(full_codegen, list), f'expected "full_codegen" to be a list, but got: {full_codegen}'
    full_codegen = [OperatorName.parse(name) for name in full_codegen]

    return full_codegen
