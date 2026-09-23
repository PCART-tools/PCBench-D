def gen_headers(
        *,
        native_functions: Sequence[NativeFunction],
        grouped_native_functions: Sequence[Union[NativeFunction, NativeFunctionsGroup]],
        static_dispatch_idx: Optional[BackendIndex],
        selector: SelectiveBuilder,
        backend_indices: Dict[DispatchKey, BackendIndex],
        core_fm: FileManager,
        cpu_fm: FileManager,
        cuda_fm: FileManager,
        ops_fm: FileManager,
        dispatch_keys: Sequence[DispatchKey],
        functions_keys: Set[DispatchKey],
        rocm: bool,
        per_operator_headers: bool,
) -> None:
    if per_operator_headers:
        gen_per_operator_headers(
            native_functions=native_functions,
            grouped_native_functions=grouped_native_functions,
            static_dispatch_idx=static_dispatch_idx,
            selector=selector,
            backend_indices=backend_indices,
            cpu_fm=cpu_fm,
            cuda_fm=cuda_fm,
            ops_fm=ops_fm,
            dispatch_keys=dispatch_keys,
            functions_keys=functions_keys,
            rocm=rocm,
        )
    else:
        gen_aggregated_headers(
            native_functions=native_functions,
            grouped_native_functions=grouped_native_functions,
            static_dispatch_idx=static_dispatch_idx,
            selector=selector,
            backend_indices=backend_indices,
            cpu_fm=cpu_fm,
            cuda_fm=cuda_fm,
            dispatch_keys=dispatch_keys,
            functions_keys=functions_keys,
            rocm=rocm,
        )

    def static_dispatch_method_headers() -> List[str]:
        return list(mapMaybe(
            lambda fn: static_dispatch_ops_header(fn, backend_index=static_dispatch_idx),
            [fn for fn in native_functions if Variant.method in fn.variants]))


    core_fm.write('TensorBody.h', lambda: {
        'static_dispatch_ops_headers': (
            static_dispatch_method_headers() if per_operator_headers
            else static_dispatch_extra_headers(static_dispatch_idx, skip_tensor_include=True)),
        'tensor_method_declarations': list(mapMaybe(ComputeTensorMethod(
            target=Target.DECLARATION, static_dispatch_backend_index=static_dispatch_idx), native_functions)),
        'tensor_method_definitions': list(mapMaybe(ComputeTensorMethod(
            target=Target.DEFINITION, static_dispatch_backend_index=static_dispatch_idx), native_functions)),
    })

    cpu_fm.write('RedispatchFunctions.h', lambda: {
        'function_redispatch_definitions': list(mapMaybe(ComputeRedispatchFunction(), native_functions)),
    })

    cpu_fm.write('RegistrationDeclarations.h', lambda: {
        'registration_declarations': [compute_registration_declarations(f, backend_indices) for f in native_functions],
    })

    cpu_fm.write('FunctionalInverses.h', lambda: {
        'view_inverse_declarations': list(mapMaybe(gen_functionalization_view_inverse_declaration, native_functions))
    })


    def gen_aten_interned_strings() -> Dict[str, str]:
        attrs = set()  # All function argument names
        names = set()  # All ATen function names
        for func in native_functions:
            names.add(str(func.func.name.name))
            # Some operators don't have a functional variant but we still create a
            # symbol without the underscore
            names.add(func.func.name.name.base)

            for arg in func.func.schema_order_arguments():
                attrs.add(arg.name)

        # These are keywords in C++, so aren't valid symbol names
        # https://en.cppreference.com/w/cpp/language/operator_alternative
        names -= set(['and', 'and_eq', 'bitand', 'bitor', 'compl', 'not',
                      'not_eq', 'or', 'or_eq', 'xor', 'xor_eq'])

        return {
            'aten_symbols': ' \\\n'.join([
                f"_(aten, {name})" for name in sorted(names)
            ]),
            'attr_symbols': ' \\\n'.join([
                f"_(attr, {name})" for name in sorted(attrs)
            ]),
        }

    core_fm.write('aten_interned_strings.h', gen_aten_interned_strings)
