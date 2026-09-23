def main() -> None:
    parser = argparse.ArgumentParser(description='Generate ATen source files')
    parser.add_argument(
        '-s',
        '--source-path',
        help='path to source directory for ATen',
        default='aten/src/ATen')
    parser.add_argument(
        '-o',
        '--output-dependencies',
        help='output a list of dependencies into the given file and exit')
    parser.add_argument(
        '-d', '--install_dir', help='output directory',
        default='build/aten/src/ATen')
    parser.add_argument(
        '--rocm',
        action='store_true',
        help='reinterpret CUDA as ROCm/HIP and adjust filepaths accordingly')
    # TODO: --op_registration_whitelist will be removed when all call-sites
    # for gen.py are moved over to using the operator YAML file for mobile
    # custom build.
    parser.add_argument(
        '--op_registration_whitelist',
        nargs='*',
        help='filter op registrations by the whitelist (if set); '
             'each item is `namespace`::`operator name` without overload name; '
             'e.g.: aten::empty aten::conv2d ...')
    parser.add_argument(
        '--op_selection_yaml_path',
        help='Provide a path to the operator selection (for custom build) YAML '
             'that contains the information about the set of selected operators '
             'and their categories (training, ...). Each operator is either a '
             'full operator name with overload or just a bare operator name. '
             'The operator names also contain the namespace prefix (e.g. aten::)')
    parser.add_argument(
        '--backend_whitelist',
        nargs='*',
        help='filter dispatch backend by the whitelist (if set), '
             'e.g.: CPU CUDA QuantizedCPU ...')
    parser.add_argument(
        '--static_dispatch_backend',
        help='generate static dispatch code for the specific backend (if set)')
    parser.add_argument(
        '--force_schema_registration',
        action='store_true',
        help='force it to generate schema-only registrations for all ops, including'
             'those that are not listed on --op_registration_whitelist')
    options = parser.parse_args()

    selector = get_custom_build_selector(
        options.op_registration_whitelist,
        options.op_selection_yaml_path,
    )

    native_yaml_path = os.path.join(options.source_path, 'native/native_functions.yaml')
    parsed_yaml = parse_native_yaml(native_yaml_path)
    native_functions, backend_indices = parsed_yaml.native_functions, parsed_yaml.backend_indices
    grouped_native_functions = get_grouped_native_functions(native_functions)
    structured_native_functions = [g for g in grouped_native_functions if isinstance(g, NativeFunctionsGroup)]

    template_dir = os.path.join(options.source_path, "templates")

    # NB: It is mandatory to NOT use os.path.join here, as the install directory
    # will eventually be ingested by cmake, which does not respect Windows style
    # path slashes.  If you switch this to use os.path.join, you'll get an error
    # like:
    #
    #   Syntax error in cmake code when parsing string
    #
    #     C:/Jenkins/workspace/pytorch-builds/pytorch-win-ws2016-cuda9-cudnn7-py3-build/build/aten/src/ATen\core/TensorMethods.h
    #
    #   Invalid character escape '\c'.
    core_install_dir = f'{options.install_dir}/core'
    pathlib.Path(core_install_dir).mkdir(parents=True, exist_ok=True)

    def make_file_manager(install_dir: str) -> FileManager:
        return FileManager(install_dir=install_dir, template_dir=template_dir, dry_run=options.output_dependencies)

    core_fm = make_file_manager(core_install_dir)
    cpu_fm = make_file_manager(options.install_dir)
    cuda_fm = make_file_manager(options.install_dir)

    extra_cuda_headers = '''\
#include <c10/cuda/CUDAGuard.h>
#include <ATen/cuda/ATenCUDAGeneral.h>
#include <ATen/cuda/CUDADevice.h>
#include <ATen/cuda/CUDAContext.h>'''
    if options.rocm:
        extra_cuda_headers = '''\
#include <ATen/hip/impl/HIPGuardImplMasqueradingAsCUDA.h>
#include <ATen/hip/ATenHIPGeneral.h>
#include <ATen/hip/HIPDevice.h>
#include <ATen/hip/HIPContext.h>'''

    dispatch_keys = [
        DispatchKey.CPU,
        DispatchKey.SparseCPU,
        DispatchKey.SparseCsrCPU,
        DispatchKey.MkldnnCPU,
        DispatchKey.CUDA,
        DispatchKey.SparseCUDA,
        DispatchKey.SparseCsrCUDA,
        DispatchKey.QuantizedCPU,
        DispatchKey.QuantizedCUDA,
        DispatchKey.CompositeImplicitAutograd,
        DispatchKey.CompositeExplicitAutograd,
        # Meta is a magic key: it is automatically generated for structured
        # kernels
        DispatchKey.Meta,
    ]
    # Only a limited set of dispatch keys get CPUFunctions.h headers generated
    # for them; this is the set
    functions_keys = {
        DispatchKey.CPU,
        DispatchKey.CUDA,
        DispatchKey.CompositeImplicitAutograd,
        DispatchKey.CompositeExplicitAutograd,
        DispatchKey.Meta,
    }
    if options.backend_whitelist:
        dispatch_keys = [k for k in dispatch_keys if is_generic_dispatch_key(k) or str(k) in options.backend_whitelist]

    static_dispatch_idx: Optional[BackendIndex] = None
    if options.static_dispatch_backend:
        static_dispatch_idx = backend_indices[DispatchKey.parse(options.static_dispatch_backend)]

    for dispatch_key in dispatch_keys:
        fm = cuda_fm if is_cuda_dispatch_key(dispatch_key) else cpu_fm

        fm.write_with_template(f'Register{dispatch_key}.cpp', 'RegisterDispatchKey.cpp', lambda: {
            'extra_cuda_headers': extra_cuda_headers if is_cuda_dispatch_key(dispatch_key) else '',
            'external_backend_headers': '',
            'namespaced_headers': f'#include <ATen/{dispatch_key}Functions.h>' if dispatch_key in functions_keys else '',
            'DispatchKey': dispatch_key,
            'dispatch_namespace': dispatch_key.lower(),
            'dispatch_helpers': dest.gen_registration_helpers(backend_indices[dispatch_key]),
            'dispatch_namespaced_definitions': list(concatMap(
                dest.RegisterDispatchKey(
                    backend_indices[dispatch_key],
                    Target.NAMESPACED_DEFINITION,
                    selector,
                    rocm=options.rocm,
                    cpp_namespace='at::native',
                    class_method_name=None),
                grouped_native_functions
            )),
            'dispatch_anonymous_definitions': list(concatMap(
                dest.RegisterDispatchKey(
                    backend_indices[dispatch_key],
                    Target.ANONYMOUS_DEFINITION,
                    selector,
                    rocm=options.rocm,
                    cpp_namespace='at::native',
                    class_method_name=None),
                grouped_native_functions
            )),
            'dispatch_registrations': list(concatMap(
                dest.RegisterDispatchKey(
                    backend_indices[dispatch_key],
                    Target.REGISTRATION,
                    selector,
                    rocm=options.rocm,
                    cpp_namespace='at::native',
                    class_method_name=None),
                grouped_native_functions
            )),
        })

        if dispatch_key in functions_keys:
            if dispatch_key in static_dispatch_keys(static_dispatch_idx):
                # See Note [Avoiding Include Cycles In Static Dispatch]
                inl_headers = ''
            else:
                inl_headers = f'#include <ATen/{dispatch_key}Functions_inl.h>'

            fm.write_with_template(f'{dispatch_key}Functions.h', 'DispatchKeyFunctions.h', lambda: {
                'dispatch_key': str(dispatch_key),
                'inline_headers_for_nonstatic_build': inl_headers,
            })
            fm.write_with_template(f'{dispatch_key}Functions_inl.h', 'DispatchKeyFunctions_inl.h', lambda: {
                'dispatch_namespace': dispatch_key.lower(),
                'dispatch_namespaced_declarations': list(concatMap(
                    dest.RegisterDispatchKey(
                        backend_indices[dispatch_key],
                        Target.NAMESPACED_DECLARATION,
                        selector,
                        rocm=options.rocm,
                        cpp_namespace='at::native',
                        class_method_name=None),
                    grouped_native_functions
                )),
            })

        del fm

    # BackendSelect is generated specially
    cpu_fm.write('RegisterBackendSelect.cpp', lambda: {
        'backend_select_method_definitions':
            list(mapMaybe(ComputeBackendSelect(Target.DEFINITION, selector), native_functions)),
        'backend_select_function_registrations':
            list(mapMaybe(ComputeBackendSelect(Target.REGISTRATION, selector), native_functions)),
    })

    cpu_fm.write('NativeMetaFunctions.h', lambda: {
        'declarations': list(mapMaybe(compute_meta_function_declaration, structured_native_functions)),
    })

    schema_selector = selector
    if options.force_schema_registration:
        schema_selector = SelectiveBuilder.get_nop_selector()
    cpu_fm.write('RegisterSchema.cpp', lambda: {
        'schema_registrations': list(mapMaybe(RegisterSchema(schema_selector), native_functions)),
    })

    def key_func(fn: NativeFunction) -> str:
        return fn.func.name.unambiguous_name()

    cpu_fm.write_sharded(
        'Operators.cpp',
        native_functions,
        key_fn=key_func,
        env_callable=lambda fn: {
            'definitions': [ComputeOperators(Target.DEFINITION)(fn)]},
        num_shards=5,
        sharded_keys={'definitions'}
    )
    cpu_fm.write('Operators.h', lambda: {
        'declarations': list(mapMaybe(ComputeOperators(
            Target.DECLARATION), native_functions)),
    })

    cpu_fm.write('Functions.h', lambda: {
        'static_dispatch_extra_headers': static_dispatch_extra_headers(static_dispatch_idx),
        'function_definitions': list(mapMaybe(ComputeFunction(
            static_dispatch_backend_index=static_dispatch_idx), native_functions)),
    })

    cpu_fm.write('Functions.cpp', lambda: {})

    core_fm.write('TensorBody.h', lambda: {
        'static_dispatch_extra_headers': static_dispatch_extra_headers(static_dispatch_idx, skip_tensor_include=True),
        'tensor_method_declarations': list(mapMaybe(ComputeTensorMethod(
            target=Target.DECLARATION, static_dispatch_backend_index=static_dispatch_idx), native_functions)),
        'tensor_method_definitions': list(mapMaybe(ComputeTensorMethod(
            target=Target.DEFINITION, static_dispatch_backend_index=static_dispatch_idx), native_functions)),
    })

    core_fm.write('TensorMethods.cpp', lambda: {})

    cpu_fm.write('RedispatchFunctions.h', lambda: {
        'function_redispatch_definitions': list(mapMaybe(ComputeRedispatchFunction(), native_functions)),
    })

    core_fm.write('ATenOpList.cpp', lambda: {
        'aten_ops': list(mapMaybe(compute_aten_op, native_functions)),
    })

    cpu_fm.write('NativeFunctions.h', lambda: {
        'native_function_declarations': list(concatMap(
            # Convert to a set first to remove duplicate kernel names.
            # Backends are allowed to repeat kernel names; only generate the declaration once!
            lambda f: list(OrderedDict.fromkeys(concatMap(
                lambda backend_idx:
                    dest.compute_native_function_declaration(f, backend_idx),
                backend_indices.values()))),
            grouped_native_functions)),
    })

    cpu_fm.write('Declarations.yaml', lambda: format_yaml([compute_declaration_yaml(f) for f in native_functions]))
    cpu_fm.write('RegistrationDeclarations.h', lambda: {
        'registration_declarations': [compute_registration_declarations(f, backend_indices) for f in native_functions],
    })

    if options.output_dependencies:
        cpu_fm.write_outputs(options.output_dependencies)
        core_fm.write_outputs(f"{options.output_dependencies}-core")
        cuda_fm.write_outputs(f"{options.output_dependencies}-cuda")
