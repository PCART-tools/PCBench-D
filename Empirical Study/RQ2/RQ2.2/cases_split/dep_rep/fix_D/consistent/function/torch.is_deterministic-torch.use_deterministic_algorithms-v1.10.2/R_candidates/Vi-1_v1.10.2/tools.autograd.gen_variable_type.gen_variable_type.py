def gen_variable_type(
    out: str,
    native_yaml_path: str,
    fns_with_diff_infos: List[NativeFunctionWithDifferentiabilityInfo],
    template_path: str,
) -> None:

    """VariableType.h and VariableType.cpp body

    This is the at::Type subclass for differentiable tensors. The
    implementation of each function dispatches to the base tensor type to
    compute the output. The grad_fn is attached to differentiable functions.
    """
    fm = FileManager(install_dir=out, template_dir=template_path, dry_run=False)
    fm.write('VariableType.h', lambda: {
        'generated_comment': "@" f'generated from {template_path}/VariableType.h'
    })

    # NOTE: see Note [Sharded File] at the top of the VariableType.cpp
    # template regarding sharding of the generated files.
    fm.write_sharded(
        'VariableType.cpp',
        [fn for fn in fns_with_diff_infos if use_derived(fn)],
        key_fn=lambda fn: cpp.name(fn.func.func),
        base_env={
            'generated_comment':
            "@" f'generated from {template_path}/VariableType.cpp',
        },
        env_callable=gen_variable_type_func,
        num_shards=5,
        sharded_keys={'type_derived_method_definitions', 'wrapper_registrations'}
    )
