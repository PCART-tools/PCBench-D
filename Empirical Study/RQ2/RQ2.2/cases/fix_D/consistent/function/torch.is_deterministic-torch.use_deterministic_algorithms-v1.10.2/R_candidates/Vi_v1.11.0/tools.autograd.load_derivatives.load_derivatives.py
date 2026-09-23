def load_derivatives(derivatives_yaml_path: str, native_yaml_path: str) -> Sequence[DifferentiabilityInfo]:
    # Do some caching as this is a deterministic function
    global _GLOBAL_LOAD_DERIVATIVE_CACHE
    key = (derivatives_yaml_path, native_yaml_path)
    if key not in _GLOBAL_LOAD_DERIVATIVE_CACHE:

        with open(derivatives_yaml_path, 'r') as f:
            definitions = yaml.load(f, Loader=YamlLoader)

        functions = parse_native_yaml(native_yaml_path).native_functions

        # What's the difference between function schema v.s. signature?
        # function schema is the complete declaration including mutability annotation / default value and etc.
        # signature is the canonical schema for a group of functions (in-place/out/functional variants)
        # that are semantically related.
        functions_by_signature: Dict[FunctionSchema, List[NativeFunction]] = defaultdict(list)
        functions_by_schema: Dict[str, NativeFunction] = dict()
        for function in functions:
            functions_by_signature[function.func.signature()].append(function)
            assert str(function.func) not in functions_by_schema
            functions_by_schema[str(function.func)] = function

        # Keep track of how many of which ops we've seen so we can
        # disambiguate them with a numeric suffix.
        op_counter = Counter[str]()

        infos = [
            create_differentiability_info(defn, functions_by_signature, functions_by_schema, op_counter)
            for defn in definitions]

        _GLOBAL_LOAD_DERIVATIVE_CACHE[key] = infos

    return _GLOBAL_LOAD_DERIVATIVE_CACHE[key]
