def load_deprecated_signatures(
    pairs: Sequence[PythonSignatureNativeFunctionPair],
    deprecated_yaml_path: str,
    *,
    method: bool,
    pyi: bool,
) -> List[PythonSignatureNativeFunctionPair]:
    # The deprecated.yaml doesn't have complete type information, we need
    # find and leverage the original ATen signature (to which it delegates
    # the call) to generate the full python signature.
    # We join the deprecated and the original signatures using type-only form.

    # native function -> type-only signature
    @with_native_function
    def signature_original(f: NativeFunction) -> str:
        # remove inplace suffix but keep outplace suffix
        opname = str(f.func.name.name.base)
        if f.func.is_out_fn():
            opname += '_out'
        if f.func.name.name.inplace and pyi:
            opname += '_'
        args = CppSignatureGroup.from_native_function(f, method=False).signature.arguments()
        # Simply ignore TensorOptionsArguments as it does not exist in deprecated.yaml.
        types = ', '.join(argument_type_str(a.argument.type)
                          for a in args if isinstance(a.argument, Argument))
        return f'{opname}({types})'

    # deprecated -> type-only native signature (according to the call order)
    def signature_deprecated(opname: str, params: List[str], call_args: List[str]) -> str:
        # create a mapping of parameter name to parameter type
        types: Dict[str, str] = {}
        for param in params:
            if param == '*':
                continue
            type, name = param.split(' ')
            types[name] = type
        # if the name in the call is not in the parameter list, assume it's
        # a literal Scalar
        rearranged_types = ', '.join(types.get(arg, 'Scalar') for arg in call_args)
        return f'{opname}({rearranged_types})'

    # group the original ATen signatures by type-only signature
    grouped: Dict[str, List[PythonSignatureNativeFunctionPair]] = defaultdict(list)
    for pair in pairs:
        grouped[signature_original(pair.function)].append(pair)

    # find matching original signatures for each deprecated signature
    results: List[PythonSignatureNativeFunctionPair] = []

    with open(deprecated_yaml_path, 'r') as f:
        deprecated_defs = yaml.load(f, Loader=YamlLoader)

    for deprecated in deprecated_defs:
        _, params = split_name_params(deprecated['name'])
        aten_name, call_args = split_name_params(deprecated['aten'])

        for pair in grouped[signature_deprecated(aten_name, params, call_args)]:
            # It uses the types from the original ATen declaration, but the
            # ordering and parameter names from the deprecated overload. Any
            # default parameter values from the original ATen declaration are
            # ignored.
            # Deprecated signature might reorder input_args and input_kwargs,
            # but never changes output_args nor TensorOptions (if any?),
            # so here we only look into these two types of args.
            python_sig = pair.signature
            src_args: Dict[str, PythonArgument] = {a.name: PythonArgument(
                name=a.name,
                type=a.type,
                default=None,
                default_init=None,
            ) for a in itertools.chain(python_sig.input_args, python_sig.input_kwargs)}

            args: List[str] = []
            input_args: List[PythonArgument] = []
            input_kwargs: List[PythonArgument] = []

            kwarg_only = False
            for param in params:
                if param == '*':
                    kwarg_only = True
                    continue
                _, param_name = param.split(' ')
                args.append(param_name)

                if param_name not in src_args:
                    # output argument
                    continue

                if not kwarg_only:
                    if not method or param_name != 'self':
                        input_args.append(src_args[param_name])
                else:
                    input_kwargs.append(src_args[param_name])

            results.append(PythonSignatureNativeFunctionPair(
                signature=PythonSignatureDeprecated(
                    name=python_sig.name,
                    input_args=tuple(input_args),
                    input_kwargs=tuple(input_kwargs),
                    output_args=python_sig.output_args,
                    tensor_options_args=python_sig.tensor_options_args,
                    method=python_sig.method,
                    deprecated_args_names=tuple(args),
                    deprecated_args_exprs=tuple(call_args),
                    returns=python_sig.returns,
                ),
                function=pair.function,
            ))

    return results
