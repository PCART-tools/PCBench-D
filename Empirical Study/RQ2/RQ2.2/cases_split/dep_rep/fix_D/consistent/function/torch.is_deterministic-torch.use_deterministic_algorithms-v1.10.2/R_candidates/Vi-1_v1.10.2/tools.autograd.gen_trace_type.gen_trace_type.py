def gen_trace_type(out: str, native_yaml_path: str, template_path: str) -> None:
    # NOTE: see Note [Sharded File] at the top of the VariableType.cpp
    # template regarding sharding of the generated files.
    fm = FileManager(install_dir=out, template_dir=template_path, dry_run=False)
    native_functions = parse_native_yaml(native_yaml_path).native_functions
    fm.write_sharded(
        'TraceType.cpp',
        [fn for fn in native_functions if cpp.name(fn.func) not in MANUAL_TRACER],
        key_fn=lambda fn: cpp.name(fn.func),
        base_env={
            'generated_comment':
            f'@generated from {template_path}/TraceType.cpp',
        },
        env_callable=gen_trace_type_func,
        num_shards=5,
        sharded_keys={'trace_method_definitions', 'trace_wrapper_registrations'}
    )
