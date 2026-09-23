def gen_inplace_or_view_type(
    out: str,
    native_yaml_path: str,
    fns_with_infos: List[NativeFunctionWithDifferentiabilityInfo],
    template_path: str
) -> None:
    # NOTE: see Note [Sharded File] at the top of the VariableType.cpp
    # template regarding sharding of the generated files.
    num_shards = 2

    fm = FileManager(install_dir=out, template_dir=template_path, dry_run=False)
    fm.write_sharded(
        'ADInplaceOrViewType.cpp',
        [fn for fn in fns_with_infos if use_derived(fn)],
        key_fn=lambda fn: fn.func.root_name,
        base_env={
            'generated_comment':
            f'@generated from {template_path}/ADInplaceOrViewType.cpp',
        },
        env_callable=gen_inplace_or_view_type_env,
        num_shards=2,
        sharded_keys={'ops_headers', 'inplace_or_view_method_definitions',
                      'inplace_or_view_wrapper_registrations'}
    )
